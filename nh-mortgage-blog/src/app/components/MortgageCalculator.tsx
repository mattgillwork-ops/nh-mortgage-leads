"use client";

import React, { useState } from "react";

interface MortgageCalculatorProps {
  articleSlug: string;
}

export default function MortgageCalculator({ articleSlug }: MortgageCalculatorProps) {
  const [homePrice, setHomePrice] = useState(400000);
  const [downPaymentPercent, setDownPaymentPercent] = useState(10);
  const [interestRate, setInterestRate] = useState(6.5);
  const [loanTerm, setLoanTerm] = useState(30);

  const downPaymentAmount = (homePrice * downPaymentPercent) / 100;
  const loanAmount = homePrice - downPaymentAmount;
  
  // Calculate Principal & Interest (P&I)
  const monthlyRate = interestRate / 100 / 12;
  const numberOfPayments = loanTerm * 12;
  
  let monthlyPayment = 0;
  if (monthlyRate > 0) {
    monthlyPayment = 
      (loanAmount * monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments)) / 
      (Math.pow(1 + monthlyRate, numberOfPayments) - 1);
  } else {
    monthlyPayment = loanAmount / numberOfPayments;
  }

  return (
    <div className="rounded-2xl border border-slate-200/80 bg-white p-6 space-y-4 shadow-sm">
      <h4 className="font-extrabold text-base text-slate-900 leading-snug">
        Live Payment Estimator
      </h4>
      
      <div className="space-y-3 text-xs font-semibold text-slate-600">
        <div>
          <div className="flex justify-between mb-1">
            <span>Home Price:</span>
            <span className="text-slate-900 font-bold">${homePrice.toLocaleString()}</span>
          </div>
          <input 
            type="range" 
            min="100000" 
            max="1500000" 
            step="10000"
            value={homePrice} 
            onChange={(e) => setHomePrice(Number(e.target.value))}
            className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-800"
          />
        </div>
        
        <div>
          <div className="flex justify-between mb-1">
            <span>Down Payment: {downPaymentPercent}%</span>
            <span className="text-slate-900 font-bold">${Math.round(downPaymentAmount).toLocaleString()}</span>
          </div>
          <input 
            type="range" 
            min="3" 
            max="30" 
            step="1"
            value={downPaymentPercent} 
            onChange={(e) => setDownPaymentPercent(Number(e.target.value))}
            className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-800"
          />
        </div>

        <div>
          <div className="flex justify-between mb-1">
            <span>Interest Rate:</span>
            <span className="text-slate-900 font-bold">{interestRate}%</span>
          </div>
          <input 
            type="range" 
            min="4" 
            max="9" 
            step="0.125"
            value={interestRate} 
            onChange={(e) => setInterestRate(Number(e.target.value))}
            className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-800"
          />
        </div>
      </div>

      <div className="border-t border-slate-100 pt-4 text-center">
        <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block mb-1">Estimated P&I Payment</span>
        <span className="text-2xl font-extrabold text-slate-900">${Math.round(monthlyPayment).toLocaleString()}</span>
        <span className="text-slate-400 text-[10px] block mt-0.5">/ month (Principal & Interest)</span>
      </div>

      <a 
        href={`https://nh-mortgage-leads.onrender.com/funnel?utm_source=nh-mortgage-blog&utm_medium=sidebar-calc&utm_campaign=${articleSlug}&price=${homePrice}&down=${downPaymentPercent}&rate=${interestRate}`}
        className="w-full inline-flex items-center justify-center px-4 h-10 rounded-xl bg-blue-800 text-white font-extrabold text-xs hover:bg-blue-900 transition-colors text-center shadow-sm"
      >
        Get Pre-Approved for This Payment →
      </a>
    </div>
  );
}
