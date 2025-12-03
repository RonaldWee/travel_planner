'use client';

import { FlightOption } from '@/lib/api';
import { formatDuration, formatPrice } from '@/lib/utils';
import { Plane } from 'lucide-react';

interface FlightListProps {
  flights: FlightOption[];
  origin?: string;
  destination?: string;
}

export default function FlightList({ flights, origin, destination }: FlightListProps) {
  if (!flights || flights.length === 0) {
    return (
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">Flight Options</h3>
        <p className="text-gray-600 dark:text-gray-400">No flight data available</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <Plane className="w-5 h-5" />
        Flight Options
      </h3>

      {origin && destination && (
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
          {origin} → {destination}
        </p>
      )}

      <div className="space-y-3">
        {flights.map((flight, index) => (
          <div
            key={index}
            className="border border-gray-200 dark:border-slate-600 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-start">
              <div>
                <div className="text-lg font-semibold text-gray-900 dark:text-white">
                  {formatPrice(flight.price, flight.currency)}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Duration: {formatDuration(flight.duration)}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  {flight.segments === 1 ? 'Direct flight' : `${flight.segments} stops`}
                </div>
              </div>
              <div className="text-xs bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 px-2 py-1 rounded">
                {flight.one_way ? 'One-way' : 'Round-trip'}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
