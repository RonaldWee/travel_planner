'use client';

import { Attraction } from '@/lib/api';
import { MapPin, Star } from 'lucide-react';

interface AttractionListProps {
  attractions: Record<string, Attraction[]>;
}

export default function AttractionList({ attractions }: AttractionListProps) {
  if (!attractions || Object.keys(attractions).length === 0) {
    return (
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">Attractions & Activities</h3>
        <p className="text-gray-600 dark:text-gray-400">No attraction data available</p>
      </div>
    );
  }

  const categoryIcons: Record<string, string> = {
    culture: '🏛️',
    landmarks: '🗼',
    nature: '🌳',
    food_districts: '🍜',
    markets: '🛍️',
    day_trips: '🚌',
    shopping: '🛒',
    entertainment: '🎭',
  };

  return (
    <div className="card">
      <h3 className="text-xl font-semibold mb-4">Attractions & Activities</h3>

      <div className="space-y-6">
        {Object.entries(attractions).map(([category, items]) => {
          if (!items || items.length === 0) return null;

          return (
            <div key={category}>
              <h4 className="text-lg font-semibold mb-3 flex items-center gap-2 capitalize">
                <span>{categoryIcons[category] || '📍'}</span>
                {category.replace('_', ' ')}
              </h4>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {items.slice(0, 6).map((attraction, index) => (
                  <div
                    key={index}
                    className="border border-gray-200 dark:border-slate-600 rounded-lg p-3 hover:shadow-md transition-shadow"
                  >
                    <h5 className="font-semibold text-gray-900 dark:text-white text-sm">
                      {attraction.name}
                    </h5>

                    {attraction.rating > 0 && (
                      <div className="flex items-center gap-1 mt-1">
                        <Star className="w-3 h-3 fill-yellow-400 stroke-yellow-400" />
                        <span className="text-xs text-gray-600 dark:text-gray-400">
                          {attraction.rating.toFixed(1)}
                        </span>
                      </div>
                    )}

                    {attraction.vicinity && (
                      <div className="flex items-center gap-1 mt-1">
                        <MapPin className="w-3 h-3 text-gray-500" />
                        <span className="text-xs text-gray-600 dark:text-gray-400">
                          {attraction.vicinity}
                        </span>
                      </div>
                    )}

                    {attraction.description && (
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-2 line-clamp-2">
                        {attraction.description}
                      </p>
                    )}
                  </div>
                ))}
              </div>

              {items.length > 6 && (
                <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                  + {items.length - 6} more {category.replace('_', ' ')}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
