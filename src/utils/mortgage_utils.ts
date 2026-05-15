/**
 * NH Mortgage Intelligence Utilities
 * Centralized logic for loan calculations, ROI, and local tax estimations.
 */

export interface MortgageInputs {
  est_value: number;
  down_payment: number;
  current_payment: number;
  annual_rate: number;
  term_years?: number;
  est_insurance_monthly?: number;
  est_tax_rate_annual?: number;
}

export interface MortgageReport {
  principal_loan_amount: number;
  monthly_pi: number; // Principal & Interest
  monthly_taxes: number;
  monthly_insurance: number;
  monthly_pmi: number;
  total_monthly_payment: number;
  monthly_savings: number;
  lifetime_roi: number;
  equity_30y: number; // Added for positive pivot
}

/**
 * Calculates a comprehensive mortgage report based on NH-specific estimates.
 */
export const calculateMortgageReport = (inputs: MortgageInputs): MortgageReport => {
  const {
    est_value,
    down_payment,
    current_payment,
    annual_rate,
    term_years = 30,
    est_insurance_monthly = 100,
    est_tax_rate_annual = 0.018, // NH Avg roughly 1.8%
  } = inputs;

  const principal = est_value - down_payment;
  const monthlyRate = (annual_rate / 100) / 12;
  const numberOfPayments = term_years * 12;

  // Monthly Principal & Interest Calculation
  let monthlyPI = 0;
  if (monthlyRate > 0) {
    monthlyPI =
      (principal * (monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments))) /
      (Math.pow(1 + monthlyRate, numberOfPayments) - 1);
  } else {
    monthlyPI = principal / numberOfPayments;
  }

  // NH Property Tax Estimate
  const monthlyTaxes = (est_value * est_tax_rate_annual) / 12;

  // PMI Estimate (if down payment < 20%)
  const pmiRate = 0.005; // 0.5% annual estimate
  const monthlyPMI = down_payment / est_value < 0.2 ? (principal * pmiRate) / 12 : 0;

  const totalMonthly = monthlyPI + monthlyTaxes + est_insurance_monthly + monthlyPMI;
  const monthlySavings = current_payment - totalMonthly;
  const lifetimeROI = monthlySavings * 12 * term_years;

  // Positive Pivot: 30-Year Equity Projection
  // Calculation: Down Payment + Principal Paid (all of it) + 3% Annual Appreciation
  const appreciationRate = 0.03;
  const futureValue = est_value * Math.pow(1 + appreciationRate, term_years);
  const equity30y = futureValue; // Since it's a 30y term, loan is paid off.

  return {
    principal_loan_amount: principal,
    monthly_pi: parseFloat(monthlyPI.toFixed(2)),
    monthly_taxes: parseFloat(monthlyTaxes.toFixed(2)),
    monthly_insurance: est_insurance_monthly,
    monthly_pmi: parseFloat(monthlyPMI.toFixed(2)),
    total_monthly_payment: parseFloat(totalMonthly.toFixed(2)),
    monthly_savings: parseFloat(monthlySavings.toFixed(2)),
    lifetime_roi: parseFloat(lifetimeROI.toFixed(2)),
    equity_30y: Math.round(equity30y),
  };
};
