'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import SearchForm from '@/components/SearchForm';
import travelPlannerAPI, { TravelPlanRequest, TravelPlanResponse } from '@/lib/api';
import { Plane, Sparkles } from 'lucide-react';

export default function Home() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: TravelPlanRequest) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await travelPlannerAPI.createPlan(data);

      // Store result in sessionStorage and navigate to plan page
      sessionStorage.setItem('travelPlan', JSON.stringify(result));
      router.push('/plan');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create travel plan');
      console.error('Planning error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 animate-fadeIn">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Plane className="w-12 h-12 text-primary-600" />
            <Sparkles className="w-8 h-8 text-yellow-500" />
          </div>
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            AI Travel Planner
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Let AI create your perfect travel itinerary with flights, hotels, attractions, and expert tips
          </p>

          <div className="mt-6 flex flex-wrap justify-center gap-4 text-sm text-gray-600 dark:text-gray-400">
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>Flight & Hotel Search</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>Personalized Itinerary</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>Budget Estimates</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>Local Tips & Culture</span>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 rounded-lg animate-fadeIn">
            <p className="font-semibold">Error</p>
            <p>{error}</p>
          </div>
        )}

        {/* Search Form */}
        <div className="animate-fadeIn">
          <SearchForm onSubmit={handleSubmit} isLoading={isLoading} />
        </div>

        {/* Features */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 animate-fadeIn">
          <div className="text-center p-6">
            <div className="text-4xl mb-3">🤖</div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">AI-Powered</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Using Claude 3.5 Sonnet via OpenRouter for intelligent planning
            </p>
          </div>

          <div className="text-center p-6">
            <div className="text-4xl mb-3">🌍</div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Real Data</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Integrates with Amadeus and Google Places for accurate information
            </p>
          </div>

          <div className="text-center p-6">
            <div className="text-4xl mb-3">⚡</div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Fast Planning</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Complete travel plan generated in minutes with CrewAI orchestration
            </p>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-sm text-gray-500 dark:text-gray-500">
          <p>Powered by CrewAI, FastAPI, OpenRouter (Claude 3.5 Sonnet), and Next.js</p>
          <p className="mt-2">MCP tools for Amadeus & Google Places integration</p>
        </footer>
      </div>
    </main>
  );
}
