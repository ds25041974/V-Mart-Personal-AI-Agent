# Rate Limit Handling Guide

## Overview
The V-Mart AI Agent now includes intelligent retry logic with exponential backoff to handle Google Gemini API rate limits (Error 429).

## What is Error 429?
- **Error Code**: 429 Resource Exhausted
- **Meaning**: You've exceeded the API's rate limits (too many requests in a short time)
- **Common Causes**:
  - Sending multiple requests too quickly
  - Large file uploads or complex analysis
  - Concurrent users making requests simultaneously

## Automatic Retry System

### How It Works
When a rate limit error occurs, the system automatically:

1. **Detects** the 429 error
2. **Waits** with exponential backoff (2s, 4s, 8s, 16s, 32s)
3. **Retries** up to 5 times
4. **Returns** a user-friendly message if all retries fail

### Retry Schedule
| Attempt | Wait Time | Total Time Elapsed |
|---------|-----------|-------------------|
| 1       | 2 seconds | 2 seconds         |
| 2       | 4 seconds | 6 seconds         |
| 3       | 8 seconds | 14 seconds        |
| 4       | 16 seconds| 30 seconds        |
| 5       | 32 seconds| 62 seconds        |

## Gemini API Free Tier Limits (2024-2025)

### Gemini 2.0 Flash (Current Model)
- **Rate Limits**:
  - 15 requests per minute (RPM)
  - 1 million tokens per minute (TPM)
  - 1,500 requests per day (RPD)

- **Quota Calculation**:
  - Each PDF analysis = 1 request
  - Each chat message = 1 request
  - Each file analysis = 1 request

### Best Practices to Avoid Rate Limits

1. **Wait Between Requests**
   - Wait 4-5 seconds between consecutive requests
   - Avoid uploading multiple PDFs rapidly

2. **Reduce File Size**
   - Keep PDFs under 10 pages when possible
   - Compress images before uploading
   - Use text-based PDFs instead of scanned images

3. **Batch Operations**
   - Instead of analyzing 10 files separately, combine them
   - Use comparison mode to analyze multiple files at once

4. **Monitor Usage**
   - Check your daily quota in Google Cloud Console
   - Review usage patterns during peak times

## User-Friendly Error Messages

When rate limit is reached after all retries, users will see:

```
⚠️ Rate limit exceeded. The API is currently busy. Please try again in a few minutes.

Tip: Try reducing the frequency of requests or wait 60 seconds before trying again.
```

## Upgrading to Paid Tier

If you frequently hit rate limits, consider upgrading:

### Pay-as-you-go Pricing
- **Gemini 2.0 Flash**: $0.075 per 1M input tokens, $0.30 per 1M output tokens
- **Higher Limits**: 
  - 1,000 RPM
  - 4 million TPM
  - No daily limit

### How to Upgrade
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Go to "Billing" settings
3. Enable billing and set up payment method
4. Your API key will automatically get higher limits

## Monitoring Rate Limits

### Check Current Usage
```bash
# View recent API requests in logs
tail -100 ~/Library/Logs/vmart-ai.log | grep "Rate limit"
```

### Track Errors
The system logs all retry attempts:
```
Rate limit hit. Retrying in 2 seconds... (Attempt 1/5)
Rate limit hit. Retrying in 4 seconds... (Attempt 2/5)
Rate limit hit. Retrying in 8 seconds... (Attempt 3/5)
```

## Technical Implementation

The retry logic is implemented in `src/agent/gemini_agent.py`:

```python
def get_response(self, prompt: str, use_context: bool = True) -> str:
    max_retries = 5
    base_delay = 2  # Start with 2 seconds
    
    for attempt in range(max_retries):
        try:
            response = self.chat_model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            if "429" in str(e) or "Resource exhausted" in str(e):
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    time.sleep(delay)
                    continue
                else:
                    return "Rate limit exceeded message"
```

## Troubleshooting

### Still Getting 429 Errors?

1. **Check API Key Validity**
   ```bash
   # Verify your API key in .env file
   cat .env | grep GEMINI_API_KEY
   ```

2. **Verify Model Availability**
   - Ensure `gemini-2.0-flash` is available in your region
   - Check [Google AI Studio](https://aistudio.google.com/) for model status

3. **Wait Longer**
   - If hitting daily quota, wait until next day (resets at midnight UTC)
   - For minute-based limits, wait 60 seconds

4. **Contact Support**
   - Visit [Google Cloud Support](https://cloud.google.com/support)
   - Report persistent rate limit issues

## Alternative Solutions

### Use Local Caching
The system could cache frequent responses to reduce API calls (future enhancement).

### Queue System
For high-volume usage, implement a request queue to control rate (future enhancement).

### Multiple API Keys
Rotate between multiple API keys for higher throughput (not recommended for free tier).

## Summary

✅ **Automatic retry** with exponential backoff (up to 5 attempts)
✅ **User-friendly messages** when limits are reached
✅ **Best practices** to avoid hitting limits
✅ **Upgrade path** to paid tier for higher limits
✅ **Monitoring** through logs and error tracking

---

**Last Updated**: November 10, 2025
**V-Mart AI Agent Version**: 1.0
**Developed by**: DSR | Inspired by: LA | Powered by: Gemini AI
