/**
 * Data Catalogue Configuration Module
 * Handles Item Master, Store Master, Competition Master, and Marketing Plan data
 * Uses IndexedDB for frontend storage and correlation analysis
 */

// IndexedDB configuration
const DB_NAME = 'VMartCatalogueDB';
const DB_VERSION = 1;
let catalogueDB = null;

// Master data types
const MASTER_TYPES = {
    ITEM: 'itemMaster',
    STORE: 'storeMaster',
    COMPETITION: 'competitionMaster',
    MARKETING: 'marketingPlan'
};

// Initialize IndexedDB
function initCatalogueDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => {
            catalogueDB = request.result;
            console.log('✅ Catalogue DB initialized');
            resolve(catalogueDB);
        };
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            console.log('🔧 Creating catalogue database schema...');
            
            // Create object stores for each master data type
            if (!db.objectStoreNames.contains('itemMaster')) {
                const itemStore = db.createObjectStore('itemMaster', { keyPath: 'id', autoIncrement: true });
                itemStore.createIndex('itemCode', 'itemCode', { unique: false });
                console.log('Created itemMaster store');
            }
            
            if (!db.objectStoreNames.contains('storeMaster')) {
                const storeStore = db.createObjectStore('storeMaster', { keyPath: 'id', autoIncrement: true });
                storeStore.createIndex('storeCode', 'storeCode', { unique: false });
                console.log('Created storeMaster store');
            }
            
            if (!db.objectStoreNames.contains('competitionMaster')) {
                const competitionStore = db.createObjectStore('competitionMaster', { keyPath: 'id', autoIncrement: true });
                competitionStore.createIndex('competitorName', 'competitorName', { unique: false });
                console.log('Created competitionMaster store');
            }
            
            if (!db.objectStoreNames.contains('marketingPlan')) {
                const marketingStore = db.createObjectStore('marketingPlan', { keyPath: 'id', autoIncrement: true });
                marketingStore.createIndex('campaignId', 'campaignId', { unique: false });
                console.log('Created marketingPlan store');
            }
            
            // Metadata store to track file info
            if (!db.objectStoreNames.contains('catalogueMetadata')) {
                db.createObjectStore('catalogueMetadata', { keyPath: 'type' });
                console.log('Created catalogueMetadata store');
            }
        };
    });
}

// Validate filename matches master type
function validateMasterFileName(filename, masterType) {
    const lowerName = filename.toLowerCase();
    const patterns = {
        'item': ['item', 'product', 'sku', 'inventory'],
        'store': ['store', 'location', 'branch', 'outlet'],
        'competition': ['competition', 'competitor', 'rival', 'competitive'],
        'marketing': ['marketing', 'campaign', 'promo', 'promotion']
    };
    
    const keywords = patterns[masterType] || [];
    return keywords.some(keyword => lowerName.includes(keyword));
}

// Get expected keywords for master type
function getMasterKeywords(masterType) {
    const patterns = {
        'item': 'item, product, sku, inventory',
        'store': 'store, location, branch, outlet',
        'competition': 'competition, competitor, rival, competitive',
        'marketing': 'marketing, campaign, promo, promotion'
    };
    return patterns[masterType] || '';
}

// Parse CSV file
function parseCSV(text) {
    const lines = text.split('\n').filter(line => line.trim());
    if (lines.length < 2) {
        throw new Error('CSV file is empty or invalid');
    }
    
    const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].match(/(".*?"|[^,]+)(?=\s*,|\s*$)/g) || [];
        const row = {};
        headers.forEach((header, index) => {
            row[header] = (values[index] || '').trim().replace(/^"|"$/g, '');
        });
        data.push(row);
    }
    
    return data;
}

// Parse master file
function parseMasterFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        const isCSV = file.name.toLowerCase().endsWith('.csv');
        
        if (!isCSV) {
            reject(new Error('Only CSV files are currently supported. Please convert Excel files to CSV format.'));
            return;
        }
        
        reader.onload = function(e) {
            try {
                const data = parseCSV(e.target.result);
                console.log(`✅ Parsed ${data.length} records from ${file.name}`);
                resolve(data);
            } catch (error) {
                console.error('Parse error:', error);
                reject(error);
            }
        };
        
        reader.onerror = () => reject(reader.error);
        reader.readAsText(file);
    });
}

// Detect incremental data (check for new/updated records)
function detectIncrementalData(existingData, newData) {
    // For now, we'll replace all data
    // In future, implement intelligent merge based on primary keys
    return {
        new: newData.length,
        updated: 0,
        deleted: 0,
        total: newData.length
    };
}

// Store data in IndexedDB
function storeMasterData(masterType, data, metadata) {
    return new Promise((resolve, reject) => {
        if (!catalogueDB) {
            reject(new Error('Database not initialized'));
            return;
        }
        
        const transaction = catalogueDB.transaction([masterType, 'catalogueMetadata'], 'readwrite');
        const store = transaction.objectStore(masterType);
        const metaStore = transaction.objectStore('catalogueMetadata');
        
        // Clear existing data
        store.clear();
        
        // Add new data
        let addedCount = 0;
        data.forEach(record => {
            try {
                store.add(record);
                addedCount++;
            } catch (e) {
                console.warn('Failed to add record:', record, e);
            }
        });
        
        // Update metadata
        metaStore.put({
            type: masterType,
            filename: metadata.filename,
            uploadDate: new Date().toISOString(),
            recordCount: addedCount,
            fileSize: metadata.fileSize
        });
        
        transaction.oncomplete = () => {
            console.log(`✅ Stored ${addedCount} records in ${masterType}`);
            resolve(addedCount);
        };
        transaction.onerror = () => {
            console.error('Transaction error:', transaction.error);
            reject(transaction.error);
        };
    });
}

// Get master data from IndexedDB
function getMasterData(masterType) {
    return new Promise((resolve, reject) => {
        if (!catalogueDB) {
            reject(new Error('Database not initialized'));
            return;
        }
        
        const transaction = catalogueDB.transaction([masterType], 'readonly');
        const store = transaction.objectStore(masterType);
        const request = store.getAll();
        
        request.onsuccess = () => {
            console.log(`📊 Retrieved ${request.result.length} records from ${masterType}`);
            resolve(request.result);
        };
        request.onerror = () => reject(request.error);
    });
}

// Get metadata
function getMetadata(masterType) {
    return new Promise((resolve, reject) => {
        if (!catalogueDB) {
            reject(new Error('Database not initialized'));
            return;
        }
        
        const transaction = catalogueDB.transaction(['catalogueMetadata'], 'readonly');
        const store = transaction.objectStore('catalogueMetadata');
        const request = store.get(masterType);
        
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

// Clear master data
function clearMasterData(masterType) {
    return new Promise((resolve, reject) => {
        if (!catalogueDB) {
            reject(new Error('Database not initialized'));
            return;
        }
        
        const transaction = catalogueDB.transaction([masterType, 'catalogueMetadata'], 'readwrite');
        const store = transaction.objectStore(masterType);
        const metaStore = transaction.objectStore('catalogueMetadata');
        
        store.clear();
        metaStore.delete(masterType);
        
        transaction.oncomplete = () => {
            console.log(`🗑️ Cleared ${masterType}`);
            resolve();
        };
        transaction.onerror = () => reject(transaction.error);
    });
}

// Get all catalogue data for Gemini
async function getAllCatalogueDataForGemini() {
    const catalogueData = {
        item: await getMasterData(MASTER_TYPES.ITEM),
        store: await getMasterData(MASTER_TYPES.STORE),
        competition: await getMasterData(MASTER_TYPES.COMPETITION),
        marketing: await getMasterData(MASTER_TYPES.MARKETING)
    };
    
    const metadata = {
        item: await getMetadata(MASTER_TYPES.ITEM),
        store: await getMetadata(MASTER_TYPES.STORE),
        competition: await getMetadata(MASTER_TYPES.COMPETITION),
        marketing: await getMetadata(MASTER_TYPES.MARKETING)
    };
    
    return {
        data: catalogueData,
        metadata: metadata,
        summary: {
            itemCount: catalogueData.item.length,
            storeCount: catalogueData.store.length,
            competitionCount: catalogueData.competition.length,
            marketingCount: catalogueData.marketing.length
        }
    };
}

// Format catalogue data for Gemini prompt
function formatCatalogueDataForPrompt(catalogueData) {
    let prompt = '\n\n📚 MASTER DATA CATALOGUE (Available for Deep Analysis):\n\n';
    
    if (catalogueData.summary.itemCount > 0) {
        prompt += `📦 ITEM MASTER (${catalogueData.summary.itemCount} records):\n`;
        prompt += JSON.stringify(catalogueData.data.item.slice(0, 100), null, 2) + '\n\n';
        if (catalogueData.summary.itemCount > 100) {
            prompt += `... and ${catalogueData.summary.itemCount - 100} more items\n\n`;
        }
    }
    
    if (catalogueData.summary.storeCount > 0) {
        prompt += `🏪 STORE MASTER (${catalogueData.summary.storeCount} records):\n`;
        prompt += JSON.stringify(catalogueData.data.store.slice(0, 100), null, 2) + '\n\n';
        if (catalogueData.summary.storeCount > 100) {
            prompt += `... and ${catalogueData.summary.storeCount - 100} more stores\n\n`;
        }
    }
    
    if (catalogueData.summary.competitionCount > 0) {
        prompt += `🎯 COMPETITION MASTER (${catalogueData.summary.competitionCount} records):\n`;
        prompt += JSON.stringify(catalogueData.data.competition.slice(0, 100), null, 2) + '\n\n';
        if (catalogueData.summary.competitionCount > 100) {
            prompt += `... and ${catalogueData.summary.competitionCount - 100} more competitors\n\n`;
        }
    }
    
    if (catalogueData.summary.marketingCount > 0) {
        prompt += `📈 MARKETING PLAN (${catalogueData.summary.marketingCount} records):\n`;
        prompt += JSON.stringify(catalogueData.data.marketing.slice(0, 100), null, 2) + '\n\n';
        if (catalogueData.summary.marketingCount > 0) {
            prompt += `... and ${catalogueData.summary.marketingCount - 100} more marketing campaigns\n\n`;
        }
    }
    
    prompt += '\n🧠 INSTRUCTIONS FOR AI:\n';
    prompt += '- Analyze this master data with deep correlation and cross-referencing\n';
    prompt += '- Provide insights that connect Item, Store, Competition, and Marketing data\n';
    prompt += '- Use actual values from the data, not assumptions\n';
    prompt += '- Give actionable recommendations based on data patterns\n\n';
    
    return prompt;
}

// Export for use in other scripts
if (typeof window !== 'undefined') {
    window.CatalogueDB = {
        init: initCatalogueDB,
        getMasterData,
        getMetadata,
        clearMasterData,
        getAllForGemini: getAllCatalogueDataForGemini,
        formatForPrompt: formatCatalogueDataForPrompt,
        MASTER_TYPES
    };
}
