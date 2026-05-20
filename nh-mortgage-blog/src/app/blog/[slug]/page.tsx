import Link from "next/link";
import { notFound } from "next/navigation";

// Define the article structure
interface Article {
  slug: string;
  title: string;
  excerpt: string;
  date: string;
  readTime: string;
  category: string;
  gradient: string;
  content: React.ReactNode;
}

// 3 fully written high-quality articles
const articles: Record<string, Article> = {
  "nhhfa-home-start-qualification-2026": {
    slug: "nhhfa-home-start-qualification-2026",
    title: "How to Qualify for the NHHFA Home Start Program in 2026",
    excerpt: "Everything you need to know about qualifying for New Hampshire Housing's premier first-time homebuyer program, including income limits, credit scores, and down payment assistance.",
    date: "May 19, 2026",
    readTime: "6 min read",
    category: "First-Time Buyer",
    gradient: "from-slate-900 to-blue-900",
    content: (
      <div className="space-y-6">
        <p>
          For many prospective homebuyers in the Granite State, saving for a down payment remains the single largest hurdle to homeownership. Fortunately, the <strong>New Hampshire Housing Finance Authority (NHHFA)</strong> offers several programs designed to bridge this gap, with the <strong>Home Start Program</strong> leading the way.
        </p>
        
        <p>
          The Home Start Program combines low-interest, fixed-rate mortgages with cash assistance options that can be applied directly to your down payment and closing costs. In this guide, we break down the 2026 qualification criteria so you know exactly what is required to secure your approval.
        </p>

        <h2 className="text-2xl font-bold font-sans text-slate-900 pt-4">1. Key Qualification Criteria</h2>
        <p>
          To qualify for the Home Start program, borrowers must meet specific requirements set by NHHFA, which are updated annually to match state economic conditions.
        </p>
        <ul className="list-disc pl-6 space-y-2">
          <li><strong>First-Time Homebuyer Status:</strong> In most cases, you must not have owned a home as your primary residence in the past three years. However, this requirement is waived in designated targeted areas of the state.</li>
          <li><strong>Minimum Credit Score:</strong> NHHFA generally requires a minimum credit score of <strong>620</strong> for standard loan options. For higher debt-to-income limits, a 640 or higher may be required.</li>
          <li><strong>Occupancy:</strong> The property must be a one- to four-family home and serve as your primary residence. Secondary homes and investment properties are not eligible.</li>
        </ul>

        <h2 className="text-2xl font-bold font-sans text-slate-900 pt-4">2. 2026 Income and Purchase Price Limits</h2>
        <p>
          Because Home Start is targeted at low- to moderate-income households, NHHFA establishes strict limits on how much your household can earn. These limits depend on the county in which you are purchasing a home and your household size.
        </p>
        
        <div className="overflow-x-auto my-6">
          <table className="min-w-full divide-y divide-slate-200 border border-slate-200/80 rounded-lg">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">County</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Income Limit (1-2 Person)</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Income Limit (3+ Person)</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Max Purchase Price</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-100 text-sm">
              <tr>
                <td className="px-4 py-3 font-semibold text-slate-900">Hillsborough</td>
                <td className="px-4 py-3">$115,200</td>
                <td className="px-4 py-3">$132,400</td>
                <td className="px-4 py-3">$485,000</td>
              </tr>
              <tr>
                <td className="px-4 py-3 font-semibold text-slate-900">Rockingham</td>
                <td className="px-4 py-3">$125,500</td>
                <td className="px-4 py-3">$144,300</td>
                <td className="px-4 py-3">$515,000</td>
              </tr>
              <tr>
                <td className="px-4 py-3 font-semibold text-slate-900">Merrimack</td>
                <td className="px-4 py-3">$108,000</td>
                <td className="px-4 py-3">$124,200</td>
                <td className="px-4 py-3">$450,000</td>
              </tr>
              <tr>
                <td className="px-4 py-3 font-semibold text-slate-900">Strafford</td>
                <td className="px-4 py-3">$112,000</td>
                <td className="px-4 py-3">$128,800</td>
                <td className="px-4 py-3">$465,000</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2 className="text-2xl font-bold font-sans text-slate-900 pt-4">3. Down Payment Assistance Options</h2>
        <p>
          One of the biggest benefits of Home Start is the ability to pair it with the **Home Flex Plus** or **Cash Up Front** assistance programs. NHHFA provides up to **3% to 4%** of the loan amount in cash assistance. 
        </p>
        <blockquote className="border-l-4 border-emerald-500 bg-emerald-50/50 p-4 rounded-r-lg font-medium text-slate-700 my-4">
          "For a $400,000 purchase, a 3% cash assistance grant translates to $12,000. This can cover your entire 3.5% down payment requirement on an FHA loan or be applied to offset title fees and prepaids."
        </blockquote>

        <h2 className="text-2xl font-bold font-sans text-slate-900 pt-4">Next Steps to Qualify</h2>
        <p>
          If you think you meet these guidelines, your first step is to get pre-qualified by an NHHFA-approved lender. They will pull your credit score, calculate your debt-to-income ratio, and confirm your county income limits.
        </p>
      </div>
    )
  },
  "nh-mortgage-credit-score-requirements": {
    slug: "nh-mortgage-credit-score-requirements",
    title: "New Hampshire Mortgage Credit Score Requirements",
    excerpt: "What credit score do you actually need to buy a home in NH? Learn the requirements for FHA, USDA, VA, and Conventional loans in the Granite State.",
    date: "May 18, 2026",
    readTime: "5 min read",
    category: "Credit & Finance",
    gradient: "from-blue-900 to-emerald-900",
    content: (
      <div className="space-y-6">
        <p>
          When you apply for a home loan, your credit score is the single most important factor determining your interest rate, monthly payment, and whether you get approved. Lenders in New Hampshire evaluate your credit history to measure the risk of lending to you.
        </p>
        <p>
          While a higher credit score is always beneficial, you don't need a perfect 800 to buy a house in the Granite State. In fact, many programs allow buyers to qualify with scores in the low 600s or high 500s. Let's look at the credit score guidelines across different loan programs.
        </p>

        <h2 className="text-2xl font-bold font-sans text-slate-900 pt-4">1. Minimum Credit Score by Loan Type</h2>
        <p>
          Each mortgage program has a base guideline for credit scores, though individual lenders may add their own extra requirements (known as "overlays").
        </p>
        
        <ul className="list-disc pl-6 space-y-3">
          <li>
            <strong>FHA Loans (Minimum Score: 580):</strong> Backed by the Federal Housing Administration, FHA loans are highly popular for first-time buyers. You can qualify with a <strong>580 credit score</strong> and only a <strong>3.5% down payment</strong>. Some lenders allow scores down to 500, but require a 10% down payment.
          </li>
          <li>
            <strong>Conventional Loans (Minimum Score: 620):</strong> Conventional loans are not backed by the federal government. They have a strict minimum cutoff of <strong>620</strong>. Borrowers with scores above 740 receive the best interest rates and lowest private mortgage insurance (PMI) premiums.
          </li>
          <li>
            <strong>USDA Loans (Minimum Score: 640):</strong> The United States Department of Agriculture offers <strong>100% financing</strong> (zero down payment) in rural New Hampshire communities. To qualify for expedited processing, USDA requires a minimum credit score of <strong>640</strong>.
          </li>
          <li>
            <strong>VA Loans (Minimum Score: None Set):</strong> VA loans are reserved for veterans, active-duty service members, and eligible spouses. While the Department of Veterans Affairs does not set a mandatory minimum score, most local NH lenders require a score of at least <strong>580 to 620</strong>.
          </li>
        </ul>

        <h2 className="text-2xl font-bold font-sans text-slate-900 pt-4">2. How Your Credit Score Affects Your Mortgage Rate</h2>
        <p>
          Your credit score has a direct impact on the interest rate you are offered. The difference between a 620 score and a 760 score can translate to thousands of dollars in interest over the life of a loan.
        </p>

        <blockquote className="border-l-4 border-blue-800 bg-blue-50/50 p-4 rounded-r-lg font-medium text-slate-700 my-4">
          "On a $350,000 Conventional loan, a borrower with a 760 score might receive an interest rate of 6.2%, while a borrower with a 630 score might receive a rate of 7.4%. This difference adds roughly $280 to the monthly mortgage payment."
        </blockquote>

        <h2 className="text-2xl font-bold font-sans text-slate-900 pt-4">3. Tips to Boost Your Score Before Buying</h2>
        <p>
          If your score is close to the threshold for a better tier, spending 3 to 6 months building it up can yield substantial savings:
        </p>
        <ol className="list-decimal pl-6 space-y-2">
          <li><strong>Reduce Credit Card Balances:</strong> Keep your credit utilization ratio below 30% on all cards. Getting it under 10% is ideal.</li>
          <li><strong>Audit Your Credit Report:</strong> Pull your credit reports from AnnualCreditReport.com and check for errors, such as incorrect late payments. File disputes immediately if you spot mistakes.</li>
          <li><strong>Do Not Open New Accounts:</strong> Avoid applying for new credit cards, auto loans, or retail accounts while preparing to buy a home, as these generate hard inquiries that can drop your score.</li>
        </ol>
      </div>
    )
  },
  "estimated-closing-costs-nh": {
    slug: "estimated-closing-costs-nh",
    title: "Granite State Closing Costs: Estimated Breakdown & Examples",
    excerpt: "Calculate your closing costs in NH. Understand transfer taxes, title fees, escrows, and how to minimize your out-of-pocket expenses when closing your loan.",
    date: "May 15, 2026",
    readTime: "7 min read",
    category: "Closing Costs",
    gradient: "from-indigo-950 to-amber-950",
    content: (
      <div className="space-y-6">
        <p>
          When purchasing a home, most buyers plan extensively for their down payment, but are often caught off guard by the **closing costs**. Closing costs are the fees and expenses associated with finalizing your mortgage and legally transferring the property title.
        </p>
        <p>
          In New Hampshire, closing costs typically average between **2% and 4%** of the home's purchase price. For a $400,000 home, this means you will need **$8,000 to $16,000** in cash, in addition to your down payment.
        </p>

        <h2 className="text-2xl font-bold font-sans text-slate-900 pt-4">1. Typical Closing Cost Breakdown in NH</h2>
        <p>
          Closing costs consist of third-party fees, lender-related fees, government taxes, and prepaid escrows. Here is a list of common items:
        </p>

        <ul className="list-disc pl-6 space-y-3">
          <li>
            <strong>New Hampshire Transfer Tax:</strong> New Hampshire levies a transfer tax on all real estate sales. The rate is <strong>$15 per $1,000</strong> of the sales price, which is legally split equally between the buyer and the seller. Thus, your share as the buyer is <strong>$7.50 per $1,000</strong>. On a $400,000 purchase, your transfer tax cost is exactly <strong>$3,000</strong>.
          </li>
          <li>
            <strong>Title Search and Title Insurance:</strong> The title company conducts a detailed search to ensure the seller has the legal right to sell the home. Buyer title services (search, settlement, and owner's title policy) usually cost between <strong>$1,200 and $2,000</strong>.
          </li>
          <li>
            <strong>Lender Fees:</strong> This includes the origination charge, underwriting fee, processing fee, and credit report fee. Expect these to total <strong>$1,000 to $1,800</strong>.
          </li>
          <li>
            <strong>Prepaids and Escrow Accounts:</strong> Lenders require you to establish an escrow account to pay future property taxes and homeowner's insurance. New Hampshire property taxes are notoriously high, and you may need to prepay 3 to 6 months of property taxes at closing, which can add <strong>$2,000 to $5,000</strong> depending on the municipality.
          </li>
        </ul>

        <h2 className="text-2xl font-bold font-sans text-slate-900 pt-4">2. Closing Cost Estimate Example</h2>
        <p>
          Let's look at a concrete example for a home purchase in Hillsborough County, NH:
        </p>

        <div className="bg-slate-100 p-6 rounded-xl border border-slate-200/60 font-mono text-xs text-slate-800 space-y-2">
          <div className="font-bold text-slate-900 border-b border-slate-200 pb-2 mb-2">ESTIMATED CLOSING COST BREAKDOWN (PURCHASE PRICE: $350,000)</div>
          <div className="flex justify-between"><span>Lender Origination & Processing:</span><span>$1,250</span></div>
          <div className="flex justify-between"><span>Appraisal Fee:</span><span>$550</span></div>
          <div className="flex justify-between"><span>Title Services & Settlement:</span><span>$1,450</span></div>
          <div className="flex justify-between"><span>NH State Transfer Tax ($7.50/$1,000):</span><span>$2,625</span></div>
          <div className="flex justify-between"><span>Homeowner's Insurance (12 months prepaid):</span><span>$1,200</span></div>
          <div className="flex justify-between"><span>Tax & Insurance Escrow Reserves:</span><span>$3,200</span></div>
          <div className="flex justify-between"><span>Recording & Admin Fees:</span><span>$175</span></div>
          <div className="flex justify-between font-bold text-slate-900 border-t border-slate-200 pt-2 mt-2"><span>TOTAL ESTIMATED CLOSING COSTS:</span><span>$10,450</span></div>
        </div>

        <h2 className="text-2xl font-bold font-sans text-slate-900 pt-4">3. How to Lower Your Out-of-Pocket Expenses</h2>
        <p>
          If you are low on cash reserves, you can utilize these strategies to minimize your out-of-pocket costs:
        </p>
        <ul className="list-disc pl-6 space-y-2">
          <li><strong>Seller Concessions:</strong> You can ask the seller to pay a portion of your closing costs (up to 3% to 6% depending on the loan type) in exchange for offering a slightly higher purchase price.</li>
          <li><strong>NHHFA Down Payment Assistance:</strong> Programs like Home Start and Home Flex allow the cash assistance grant to be applied directly to closing costs.</li>
          <li><strong>Lender Credits:</strong> The lender may offer to cover your closing costs in exchange for a slightly higher interest rate.</li>
        </ul>
      </div>
    )
  }
};

export async function generateStaticParams() {
  return Object.keys(articles).map((slug) => ({
    slug: slug,
  }));
}

interface PageProps {
  params: Promise<{ slug: string }>;
}

export default async function ArticlePage({ params }: PageProps) {
  const { slug } = await params;
  const article = articles[slug];

  if (!article) {
    notFound();
  }

  return (
    <div className="flex-1 flex flex-col font-sans">
      {/* Navbar */}
      <header className="sticky top-0 z-50 glass-panel border-b border-slate-200/80">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/" className="w-10 h-10 rounded-xl bg-gradient-to-tr from-navy-900 to-blue-800 flex items-center justify-center text-white font-extrabold text-lg shadow-sm">
              NH
            </Link>
            <div>
              <span className="font-extrabold text-xl tracking-tight text-slate-900 block">NH Mortgage Journal</span>
              <span className="text-[10px] uppercase font-bold tracking-widest text-emerald-500 block -mt-1">Granite State Guide</span>
            </div>
          </div>
          
          <nav className="flex items-center gap-6">
            <Link href="/" className="text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors">
              ← Back to Articles
            </Link>
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl mx-auto px-6 py-12 w-full grid grid-cols-1 lg:grid-cols-12 gap-10">
        {/* Editorial Post (Columns 1-8) */}
        <article className="lg:col-span-8 space-y-8">
          {/* Post Header */}
          <div className="space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-100 text-blue-800 text-xs font-semibold">
              {article.category}
            </div>
            
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-slate-900 font-sans leading-tight">
              {article.title}
            </h1>
            
            <div className="flex items-center gap-4 text-xs font-bold text-slate-400">
              <span>{article.date}</span>
              <span className="h-1 w-1 rounded-full bg-slate-300"></span>
              <span>{article.readTime}</span>
              <span className="h-1 w-1 rounded-full bg-slate-300"></span>
              <span className="text-slate-500">By Financial Editorial Team</span>
            </div>
          </div>

          {/* Graphic Banner */}
          <div className={`w-full h-48 md:h-64 rounded-2xl bg-gradient-to-tr ${article.gradient} flex items-center justify-center overflow-hidden text-white border border-slate-200/50 shadow-inner relative`}>
            <div className="absolute inset-0 w-full h-full opacity-10 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px]"></div>
            <div className="text-center px-6 relative z-10 max-w-md">
              <p className="text-lg font-medium opacity-90 leading-relaxed font-sans italic">
                "{article.excerpt}"
              </p>
            </div>
          </div>

          {/* Editorial Content (Georgia Serif) */}
          <div className="font-serif text-slate-700 text-lg leading-relaxed space-y-6 max-w-none prose prose-slate">
            {article.content}
          </div>
        </article>

        {/* Article Sidebar (Columns 9-12) */}
        <aside className="lg:col-span-4 space-y-8">
          {/* Main CTA: Pre-approval Funnel */}
          <div className="glass-panel rounded-2xl p-8 border border-slate-200/85 relative overflow-hidden shadow-lg shadow-slate-100/50">
            <div className="absolute -top-12 -right-12 w-24 h-24 rounded-full bg-blue-500/10 blur-xl"></div>
            <div className="absolute -bottom-12 -left-12 w-24 h-24 rounded-full bg-emerald-500/10 blur-xl"></div>
            
            <div className="relative z-10 space-y-5">
              <div className="inline-flex items-center px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 text-[10px] font-bold tracking-widest uppercase">
                NH First-Time Buyers
              </div>
              
              <h3 className="text-xl font-extrabold tracking-tight text-slate-900 leading-tight">
                Ready to take the next step?
              </h3>
              
              <p className="text-slate-600 font-medium text-xs leading-relaxed">
                Connect with local lenders, compare interest rates, and secure your pre-approval questionnaire. It's completely free.
              </p>

              <a 
                href={`https://nh-mortgage-leads.onrender.com/funnel?utm_source=nh-mortgage-blog&utm_medium=article-sidebar&utm_campaign=${article.slug}`}
                className="w-full inline-flex items-center justify-center px-5 h-11 rounded-xl bg-amber-600 text-white font-extrabold text-sm hover:bg-amber-700 transition-all shadow-md shadow-amber-600/15 text-center"
              >
                Apply for Pre-Approval <span>&nbsp;→</span>
              </a>
            </div>
          </div>

          {/* Secondary CTA: Top 10 Lender List */}
          <div className="rounded-2xl border border-slate-200/80 bg-white p-8 space-y-5 shadow-sm">
            <h4 className="font-extrabold text-base text-slate-900 leading-snug">
              Unbiased Lender Comparison
            </h4>
            
            <p className="text-slate-500 font-medium text-xs leading-relaxed">
              We reviewed and ranked the top 10 local and national mortgage institutions in New Hampshire for 2026.
            </p>
            
            <a 
              href={`https://nh-financial-review.onrender.com/?utm_source=nh-mortgage-blog&utm_medium=article-sidebar&utm_campaign=${article.slug}`}
              className="w-full inline-flex items-center justify-center px-4 h-10 rounded-lg border border-slate-200 font-bold text-xs text-slate-700 hover:bg-slate-50 hover:text-slate-900 transition-colors text-center"
            >
              Compare the Top 10 Lenders
            </a>
          </div>

          {/* Author/Editorial Panel */}
          <div className="rounded-2xl border border-slate-200/80 bg-slate-50 p-6 space-y-4">
            <h4 className="font-bold text-xs uppercase tracking-wider text-slate-400">
              Editorial Policy
            </h4>
            <p className="text-slate-500 font-medium text-xs leading-relaxed">
              Our guides are written by mortgage professionals and financial analysts. We do not accept payment for editorial reviews or listings.
            </p>
          </div>
        </aside>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200/80 bg-white py-12 text-slate-500">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-md bg-navy-900 flex items-center justify-center text-white font-extrabold text-xs">
                NH
              </div>
              <span className="font-bold text-slate-800 text-sm">NH Mortgage Journal</span>
            </div>
            <p className="text-xs font-medium max-w-sm">
              Providing free, high-quality mortgage guides and tools for home buyers across the state of New Hampshire.
            </p>
          </div>
          
          <div className="flex flex-col md:items-end gap-2 text-xs font-semibold">
            <div className="flex items-center gap-4">
              <a href="https://nh-financial-review.onrender.com" className="hover:text-slate-800">Lender Reviews</a>
              <span>•</span>
              <a href="https://nh-mortgage-leads.onrender.com/funnel" className="hover:text-slate-800">Get Pre-Approved</a>
            </div>
            <p className="text-[10px] font-medium text-slate-400 pt-1">
              &copy; {new Date().getFullYear()} NH Mortgage Journal. All rights reserved. Not affiliated with New Hampshire Housing Finance Authority.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
