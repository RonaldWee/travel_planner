'use client';

import { BudgetEstimate } from '@/lib/api';
import { formatPrice } from '@/lib/utils';
import { DollarSign } from 'lucide-react';

interface BudgetSummaryProps {
  budgets: {
    tight?: BudgetEstimate;
    moderate?: BudgetEstimate;
    flexible?: BudgetEstimate;
  };
}

export default function BudgetSummary({ budgets }: BudgetSummaryProps) {
  if (!budgets || Object.keys(budgets).length === 0) {
    return (
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">Budget Estimates</h3>
        <p className="text-gray-600 dark:text-gray-400">No budget data available</p>
      </div>
    );
  }

  const tierConfig = {
    tight: { label: 'Budget', color: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200' },
    moderate: { label: 'Mid-Range', color: 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200' },
    flexible: { label: 'Comfortable', color: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200' },
  };

  return (
    <div className="card">
      <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <DollarSign className="w-5 h-5" />
        Budget Estimates
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {Object.entries(budgets).map(([tier, budget]) => {
          const config = tierConfig[tier as keyof typeof tierConfig];
          if (!budget) return null;

          return (
            <div
              key={tier}
              className="border border-gray-200 dark:border-slate-600 rounded-lg p-4"
            >
              <div className={`inline-block px-3 py-1 rounded-full text-sm font-semibold mb-3 ${config.color}`}>
                {config.label}
              </div>

              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Daily Total:</span>
                  <span className="font-semibold">{formatPrice(budget.daily_total)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-xs text-gray-500 dark:text-gray-500">Meals:</span>
                  <span className="text-xs">{formatPrice(budget.meals)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-xs text-gray-500 dark:text-gray-500">Transport:</span>
                  <span className="text-xs">{formatPrice(budget.transport)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-xs text-gray-500 dark:text-gray-500">Accommodation:</span>
                  <span className="text-xs">{formatPrice(budget.accommodation)}</span>
                </div>
                {budget.airport_transfer && (
                  <div className="flex justify-between pt-2 border-t border-gray-200 dark:border-slate-600">
                    <span className="text-xs text-gray-500 dark:text-gray-500">Airport Transfer:</span>
                    <span className="text-xs">{formatPrice(budget.airport_transfer)}</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <p className="text-xs text-gray-500 dark:text-gray-500 mt-4 text-center">
        Estimates based on typical traveler budgets. Actual costs may vary.
      </p>
    </div>
  );
}
