"""
Automated Store Data Update Scheduler
Schedules periodic updates for weather data and store information
"""

import os
import threading
import time
from datetime import datetime

import schedule
from src.stores import StoreAnalyzer, StoreDatabase, WeatherPeriod, WeatherService


class StoreUpdateScheduler:
    """Scheduler for automatic store data updates"""

    def __init__(self):
        """Initialize scheduler with database and services"""
        self.db = StoreDatabase("data/stores.db")
        self.weather_service = WeatherService(os.getenv("OPENWEATHER_API_KEY"))
        self.analyzer = StoreAnalyzer(self.db)
        self.running = False
        self.thread = None

    def update_weather_data(self):
        """Update weather data for all V-Mart stores"""
        print(f"[{datetime.now()}] Starting weather data update...")

        try:
            stores = self.db.get_all_vmart_stores()
            updated_count = 0

            for store in stores:
                try:
                    # Get current weather
                    weather = self.weather_service.get_current_weather(store.location)

                    if weather:
                        # Save to database
                        self.db.add_weather_data(weather)
                        updated_count += 1
                        print(f"  ✓ Updated weather for {store.store_name}")

                    # Rate limit API calls
                    time.sleep(1)

                except Exception as e:
                    print(f"  ✗ Error updating weather for {store.store_name}: {e}")

            print(
                f"[{datetime.now()}] Weather update complete: {updated_count}/{len(stores)} stores"
            )

        except Exception as e:
            print(f"[{datetime.now()}] Weather update failed: {e}")

    def update_proximity_analysis(self):
        """Update competitor proximity analysis for all stores"""
        print(f"[{datetime.now()}] Starting proximity analysis update...")

        try:
            analyses = self.analyzer.analyze_all_vmart_stores(radius_km=5.0)
            print(
                f"[{datetime.now()}] Proximity analysis complete: {len(analyses)} stores analyzed"
            )

            # Log summary
            total_competitors = sum(a.get_competitor_count() for a in analyses)
            print(f"  Total competitors found: {total_competitors}")

        except Exception as e:
            print(f"[{datetime.now()}] Proximity analysis failed: {e}")

    def daily_summary(self):
        """Generate and log daily summary"""
        print(f"[{datetime.now()}] Generating daily summary...")

        try:
            summary = self.analyzer.get_competition_summary()
            print(f"  V-Mart Stores: {summary['total_vmart_stores']}")
            print(f"  Competitor Stores: {summary['total_competitor_stores']}")
            print(f"  Cities: {summary['unique_cities']}")
            print(f"  Top 3 Cities: {summary['top_10_cities'][:3]}")

        except Exception as e:
            print(f"[{datetime.now()}] Daily summary failed: {e}")

    def schedule_tasks(self):
        """Schedule all update tasks"""
        # Weather updates every 3 hours
        schedule.every(3).hours.do(self.update_weather_data)

        # Proximity analysis daily at 2 AM
        schedule.every().day.at("02:00").do(self.update_proximity_analysis)

        # Daily summary at 6 AM
        schedule.every().day.at("06:00").do(self.daily_summary)

        # Initial run
        print("=" * 60)
        print("Store Update Scheduler Initialized")
        print("=" * 60)
        print("Scheduled tasks:")
        print("  • Weather updates: Every 3 hours")
        print("  • Proximity analysis: Daily at 2:00 AM")
        print("  • Daily summary: Daily at 6:00 AM")
        print("=" * 60)

        # Run initial updates
        print("\nRunning initial updates...")
        self.update_weather_data()
        time.sleep(5)  # Brief pause
        self.update_proximity_analysis()

    def run(self):
        """Run the scheduler"""
        self.running = True
        self.schedule_tasks()

        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def start(self):
        """Start scheduler in background thread"""
        if not self.running:
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            print("✓ Store Update Scheduler started in background")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("✓ Store Update Scheduler stopped")


# Global scheduler instance
_scheduler_instance = None


def get_scheduler():
    """Get or create scheduler instance"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = StoreUpdateScheduler()
    return _scheduler_instance


def start_store_scheduler():
    """Start the store update scheduler"""
    scheduler = get_scheduler()
    scheduler.start()
    return scheduler


if __name__ == "__main__":
    # Run scheduler standalone
    print("Starting Store Update Scheduler...")
    scheduler = StoreUpdateScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        print("\nShutting down scheduler...")
        scheduler.stop()
