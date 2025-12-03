'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { TravelPlanResponse } from '@/lib/api';
import FlightList from '@/components/FlightList';
import HotelList from '@/components/HotelList';
import BudgetSummary from '@/components/BudgetSummary';
import AttractionList from '@/components/AttractionList';
import ItineraryView from '@/components/ItineraryView';
import TipsSection from '@/components/TipsSection';
import { ArrowLeft, Download, Share2, MapPin, Clock } from 'lucide-react';

export default function PlanPage() {
  const router = useRouter();
  const [plan, setPlan] = useState<TravelPlanResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Retrieve plan from sessionStorage
    const storedPlan = sessionStorage.getItem('travelPlan');

    if (storedPlan) {
      try {
        setPlan(JSON.parse(storedPlan));
      } catch (err) {
        console.error('Failed to parse travel plan:', err);
        router.push('/');
      }
    } else {
      router.push('/');
    }

    setLoading(false);
  }, [router]);

  const handleNewPlan = () => {
    sessionStorage.removeItem('travelPlan');
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading your travel plan...</p>
        </div>
      </div>
    );
  }

  if (!plan) {
    return null;
  }

  return (
    <main className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={handleNewPlan}
            className="flex items-center gap-2 text-primary-600 hover:text-primary-700 mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Create New Plan</span>
          </button>

          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <MapPin className="w-10 h-10 text-primary-600" />
                {plan.destination}
              </h1>
              {plan.origin && (
                <p className="text-lg text-gray-600 dark:text-gray-400 mt-2">
                  From {plan.origin}
                </p>
              )}
            </div>

            <div className="flex gap-3">
              <button
                className="btn-secondary flex items-center gap-2"
                onClick={() => {
                  const planText = JSON.stringify(plan, null, 2);
                  const blob = new Blob([planText], { type: 'application/json' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = `travel-plan-${plan.destination}.json`;
                  a.click();
                }}
              >
                <Download className="w-4 h-4" />
                Export
              </button>
            </div>
          </div>

          {/* Meta info */}
          <div className="flex flex-wrap gap-4 mt-4 text-sm text-gray-600 dark:text-gray-400">
            {plan.best_dates && (
              <div className="flex items-center gap-2">
                <span className="font-semibold">Best Time:</span>
                <span>{plan.best_dates}</span>
              </div>
            )}
            {plan.execution_time && (
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4" />
                <span>Generated in {plan.execution_time.toFixed(1)}s</span>
              </div>
            )}
          </div>
        </div>

        {/* Weather Summary */}
        {plan.weather_summary && (
          <div className="card mb-6 animate-fadeIn">
            <h3 className="text-lg font-semibold mb-2">Weather & Best Time to Visit</h3>
            <p className="text-gray-700 dark:text-gray-300">{plan.weather_summary}</p>
          </div>
        )}

        {/* Flight & Hotel Side by Side */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6 animate-fadeIn">
          <FlightList
            flights={plan.flight_options}
            origin={plan.origin}
            destination={plan.destination}
          />
          <HotelList hotels={plan.hotel_options} />
        </div>

        {/* Budget */}
        <div className="mb-6 animate-fadeIn">
          <BudgetSummary budgets={plan.budget_estimate} />
        </div>

        {/* Attractions */}
        <div className="mb-6 animate-fadeIn">
          <AttractionList attractions={plan.attractions} />
        </div>

        {/* Itinerary - Full Width */}
        <div className="mb-6 animate-fadeIn">
          <ItineraryView itinerary={plan.itinerary} />
        </div>

        {/* Tips */}
        <div className="mb-6 animate-fadeIn">
          <TipsSection tips={plan.tips} />
        </div>

        {/* Back to top */}
        <div className="text-center mt-12">
          <button
            onClick={handleNewPlan}
            className="btn-primary"
          >
            Plan Another Trip
          </button>
        </div>
      </div>
    </main>
  );
}
