'use client';

import { HotelOption } from '@/lib/api';
import { formatPrice } from '@/lib/utils';
import { Hotel, MapPin, Star } from 'lucide-react';

interface HotelListProps {
  hotels: HotelOption[];
}

export default function HotelList({ hotels }: HotelListProps) {
  if (!hotels || hotels.length === 0) {
    return (
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">Accommodation Options</h3>
        <p className="text-gray-600 dark:text-gray-400">No hotel data available</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <Hotel className="w-5 h-5" />
        Accommodation Options
      </h3>

      <div className="space-y-3">
        {hotels.map((hotel, index) => (
          <div
            key={index}
            className="border border-gray-200 dark:border-slate-600 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h4 className="font-semibold text-gray-900 dark:text-white">{hotel.name}</h4>
                <div className="flex items-center gap-2 mt-1 text-sm text-gray-600 dark:text-gray-400">
                  <Star className="w-4 h-4 fill-yellow-400 stroke-yellow-400" />
                  <span>{hotel.rating} stars</span>
                </div>
                <div className="flex items-center gap-2 mt-1 text-sm text-gray-600 dark:text-gray-400">
                  <MapPin className="w-4 h-4" />
                  <span>{hotel.area}</span>
                </div>
              </div>

              <div className="text-right">
                <div className="text-lg font-semibold text-gray-900 dark:text-white">
                  {formatPrice(hotel.price_per_night, hotel.currency)}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400">per night</div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Total: {formatPrice(hotel.total_price, hotel.currency)}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
