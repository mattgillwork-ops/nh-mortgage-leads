import React from 'react';

const lenders = [
  {
    id: 'nextgen',
    name: 'NH Mortgage Journal (Powered by NextGen)',
    rating: 5.0,
    badge: 'Best Overall in NH',
    description: 'Our top recommendation. An independent, Nashua-based engine that compares rates across wholesale channels to find the absolute lowest APR for NH residents. Exceptional local knowledge and access to NHHFA Home Start programs.',
    pros: ['Direct access to wholesale rates', 'NHHFA approved & first-time buyer experts', 'Sovereign pre-approval engine', 'Extremely fast local closing times'],
    cons: ['Limited to NH and surrounding New England states'],
    ctaText: 'Calculate Your NH Rate',
    ctaLink: 'https://nh-mortgage-leads.onrender.com/funnel?utm_source=nh-financial-review&utm_medium=listicle&utm_campaign=top-10-lenders',
    isPrimary: true,
  },
  {
    id: 'rocket',
    name: 'Rocket Mortgage',
    rating: 4.6,
    badge: 'Best Digital Experience',
    description: 'A national powerhouse known for its seamless online application process. Great for tech-savvy borrowers who want to handle everything from their smartphone.',
    pros: ['Excellent mobile app', 'Fast online pre-approval', 'Customizable loan terms'],
    cons: ['Can have higher fees', 'Lacks localized NH market expertise'],
    ctaText: 'Check Rocket Rates',
    ctaLink: '/out/rocket',
    isPrimary: false,
  },
  {
    id: 'better',
    name: 'Better.com',
    rating: 4.5,
    badge: 'Best for No Origination Fees',
    description: 'Better.com stands out by eliminating traditional lender fees and offering a fully digital process. They provide aggressive rate matching.',
    pros: ['No origination or lender fees', 'Fast underwriting', '24/7 customer support'],
    cons: ['Online only (no physical branches)', 'May not support complex financial situations'],
    ctaText: 'Check Better Rates',
    ctaLink: '/out/better',
    isPrimary: false,
  },
  {
    id: 'cmg',
    name: 'CMG Home Loans',
    rating: 4.4,
    badge: 'Best for Unique Loan Products',
    description: 'Known for their "All In One Loan" and strong presence in New Hampshire. They are a solid choice for borrowers needing creative financing solutions.',
    pros: ['Innovative loan options', 'Good local presence', 'First-time buyer friendly'],
    cons: ['Rates can sometimes be higher than wholesale brokers'],
    ctaText: 'Check CMG Rates',
    ctaLink: '/out/cmg',
    isPrimary: false,
  },
  {
    id: 'navyfederal',
    name: 'Navy Federal Credit Union',
    rating: 4.8,
    badge: 'Best for Military & Veterans',
    description: 'The top choice for active military and veterans seeking VA loans. They offer exceptional rates and zero down payment options for eligible borrowers.',
    pros: ['Industry-leading VA loan rates', 'No PMI requirements', 'Excellent customer service'],
    cons: ['Requires military affiliation to join', 'Physical branches are scarce in NH'],
    ctaText: 'Check Navy Federal Rates',
    ctaLink: '/out/navyfederal',
    isPrimary: false,
  },
  {
    id: 'sofi',
    name: 'SoFi',
    rating: 4.5,
    badge: 'Best for Jumbo Loans',
    description: 'Ideal for buyers looking at high-value properties in NH (like the Seacoast or Lakes Region). SoFi offers competitive rates on high-balance loans with quick pre-approvals.',
    pros: ['Low rates for jumbo loans', 'Flexible down payment options', 'Member discounts available'],
    cons: ['Strict credit requirements (typically 680+)', 'No physical branches'],
    ctaText: 'Check SoFi Rates',
    ctaLink: '/out/sofi',
    isPrimary: false,
  },
  {
    id: 'chase',
    name: 'Chase Bank',
    rating: 4.3,
    badge: 'Best for Low Down Payments',
    description: 'With their DreaMaker mortgage requiring as little as 3% down, Chase is a strong contender for first-time buyers with limited cash on hand.',
    pros: ['Low down payment programs', 'Homebuyer grants available', 'Robust online dashboard'],
    cons: ['Slower underwriting times', 'Rates often higher than wholesale'],
    ctaText: 'Check Chase Rates',
    ctaLink: '/out/chase',
    isPrimary: false,
  },
  {
    id: 'fairway',
    name: 'Fairway Independent Mortgage',
    rating: 4.6,
    badge: 'Best FHA Local Expertise',
    description: 'Fairway operates several local branches in New Hampshire and specializes in government-backed loans (FHA, USDA, VA) for borrowers with less-than-perfect credit.',
    pros: ['Highly localized NH presence', 'Fast closing guarantees', 'Great for FHA/USDA loans'],
    cons: ['Higher origination fees', 'Servicing is often transferred'],
    ctaText: 'Check Fairway Rates',
    ctaLink: '/out/fairway',
    isPrimary: false,
  },
  {
    id: 'stmarys',
    name: "St. Mary's Bank",
    rating: 4.7,
    badge: 'Best NH Credit Union',
    description: 'The nation’s first credit union, based right here in Manchester. They offer incredible localized service, portfolio loans, and community-focused lending.',
    pros: ['Incredible local customer service', 'Portfolio lending for unique properties', 'Low fees'],
    cons: ['Must become a member', 'Slower technology interface'],
    ctaText: "Check St. Mary's Rates",
    ctaLink: '/out/stmarys',
    isPrimary: false,
  },
  {
    id: 'boa',
    name: 'Bank of America',
    rating: 4.1,
    badge: 'Best for Existing Customers',
    description: 'For borrowers who already bank with BoA, their Preferred Rewards program can offer significant discounts on mortgage origination fees.',
    pros: ['Discounts for existing customers', 'Grants for low-income buyers', 'Massive branch network'],
    cons: ['Slowest closing times', 'Rigid underwriting standards'],
    ctaText: 'Check BoA Rates',
    ctaLink: '/out/boa',
    isPrimary: false,
  },
];

export default function Home() {
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Who is the best mortgage lender in New Hampshire for 2026?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Based on our independent review, NH Mortgage Journal (Powered by NextGen) is rated 5.0/5.0 and ranked #1 for its direct access to wholesale interest rates, fast local closings, and expertise with first-time homebuyer programs."
        }
      },
      {
        "@type": "Question",
        "name": "What is the NHHFA (New Hampshire Housing Finance Authority)?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "The NHHFA provides down payment and closing cost assistance programs (like Home Start and Home Flex Plus) for low-to-moderate income homebuyers in New Hampshire, helping them cover upfront acquisition costs."
        }
      },
      {
        "@type": "Question",
        "name": "Should I use a local mortgage broker or a national bank in New Hampshire?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Local mortgage brokers can shop wholesale channels to find lower interest rates tailored to the New Hampshire market. National banks offer convenience and digital tools, but may lack local market insights or carry higher margins."
        }
      }
    ]
  };

  const localBusinessSchema = {
    "@context": "https://schema.org",
    "@type": "FinancialService",
    "name": "NH Mortgage Journal",
    "alternateName": "NextGen Mortgage NH",
    "description": "Providing independent mortgage analysis, lender reviews, and home purchase pre-approvals for Granite State buyers.",
    "url": "https://nh-financial-review.onrender.com",
    "telephone": "+1-603-555-0199",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "100 Elm Street",
      "addressLocality": "Manchester",
      "addressRegion": "NH",
      "postalCode": "03101",
      "addressCountry": "US"
    },
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": 42.9912,
      "longitude": -71.4633
    },
    "openingHoursSpecification": {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
      ],
      "opens": "09:00",
      "closes": "17:00"
    },
    "priceRange": "$$"
  };

  return (
    <div className="flex-1 flex flex-col font-sans">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(localBusinessSchema) }}
      />
      {/* Navbar */}
      <header className="sticky top-0 z-50 glass-panel border-b border-slate-200/80">
        <div className="max-w-4xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-navy-900 to-blue-800 flex items-center justify-center text-white font-extrabold text-lg shadow-sm">
              FR
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight text-slate-900 block">NH Financial Review</span>
              <span className="text-[10px] uppercase font-bold tracking-widest text-blue-800 block -mt-1">Independent Mortgage Analysis</span>
            </div>
          </div>
          
          <nav className="flex items-center gap-6">
            <a 
              href="https://nh-mortgage-blog.onrender.com" 
              className="text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors"
            >
              Blog Guides
            </a>
          </nav>
        </div>
      </header>

      {/* Hero Header */}
      <section className="bg-gradient-to-b from-slate-100 to-[#f8fafc] border-b border-slate-200/50 py-12">
        <div className="max-w-4xl mx-auto px-6">
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-extrabold tracking-tight text-slate-950 font-serif leading-tight mb-6">
            Top 10 Best Mortgage Lenders in New Hampshire (2026)
          </h1>
          
          <div className="flex items-center gap-4 border-b border-slate-200/80 pb-6">
            <div className="w-10 h-10 rounded-full bg-slate-200 flex items-center justify-center font-bold text-slate-600 text-sm">
              FR
            </div>
            <div className="flex flex-col text-xs font-semibold">
              <span className="text-slate-900">By NHFR Editorial Review Team</span>
              <span className="text-slate-400">Updated: May 19, 2026 • 7 min read</span>
            </div>
          </div>

          <div className="mt-6 text-slate-700 text-base md:text-lg leading-relaxed space-y-4">
            <p>
              When you're buying a home in New Hampshire, securing the right mortgage is just as important as finding the perfect property. A lower interest rate can save you tens of thousands of dollars over the life of your loan, while a highly responsive lender can mean the difference between winning a bidding war in Manchester or missing out entirely.
            </p>
            <p>
              To help you navigate the highly competitive 2026 Granite State housing market, our editorial team analyzed dozens of national and local lenders. We weighed current rates, access to NHHFA Home Start programs, closing speeds, and customer satisfaction to bring you our definitive top picks.
            </p>
          </div>
        </div>
      </section>

      {/* Sticky Table of Contents Jump Links */}
      <div className="sticky top-20 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-sm py-4">
        <div className="max-w-4xl mx-auto px-6 flex items-center gap-3 overflow-x-auto whitespace-nowrap scrollbar-none">
          <span className="text-xs uppercase font-extrabold tracking-widest text-slate-400 mr-2">Top 5 Picks:</span>
          {lenders.slice(0, 5).map((lender, i) => (
            <a 
              key={lender.id}
              href={`#${lender.id}`}
              className="inline-flex items-center px-3 h-8 rounded-lg bg-slate-50 border border-slate-200/60 text-xs font-bold text-blue-800 hover:bg-blue-50 hover:border-blue-200 transition-colors"
            >
              #{i+1} {lender.name.split(' (')[0]}
            </a>
          ))}
        </div>
      </div>

      {/* Comparison List Content */}
      <div className="max-w-4xl mx-auto px-6 py-12 space-y-8">
        <div className="flex flex-col gap-8">
          {lenders.map((lender, index) => (
            <article 
              id={lender.id} 
              key={lender.id} 
              className={`relative overflow-hidden rounded-2xl border bg-white p-8 hover-lift ${
                lender.isPrimary 
                  ? 'border-blue-800 shadow-md shadow-blue-800/5 ring-1 ring-blue-800/10' 
                  : 'border-slate-200/80 shadow-sm'
              }`}
            >
              {/* Top Rated Ribbon */}
              {lender.isPrimary && (
                <div className="absolute top-0 right-0 bg-blue-800 text-white font-extrabold text-[10px] tracking-widest uppercase px-6 py-1.5 rounded-bl-xl border-l border-b border-blue-900/10 shadow-sm">
                  #1 RATED LENDER
                </div>
              )}
              
              <div className="flex flex-col md:flex-row justify-between items-start gap-4 mb-6">
                <div className="space-y-2">
                  <h2 className="text-xl md:text-2xl font-extrabold tracking-tight text-slate-900 font-serif leading-snug">
                    {index + 1}. {lender.name}
                  </h2>
                  <span className={`inline-flex px-2.5 py-1 rounded-md text-[10px] font-bold tracking-wider uppercase border ${
                    lender.isPrimary 
                      ? 'bg-blue-50 border-blue-100 text-blue-800' 
                      : 'bg-slate-50 border-slate-200 text-slate-600'
                  }`}>
                    {lender.badge}
                  </span>
                </div>
                
                {/* Rating Block */}
                <div className="flex items-center gap-1.5 self-start bg-slate-50 border border-slate-200/60 px-3 py-1.5 rounded-xl">
                  <span className="text-amber-500 font-bold text-sm">★</span>
                  <span className="text-slate-900 font-extrabold text-sm leading-none">{lender.rating.toFixed(1)}</span>
                  <span className="text-slate-400 text-xs font-bold">/ 5.0</span>
                </div>
              </div>

              <p className="text-slate-600 font-medium text-sm md:text-base leading-relaxed mb-6">
                {lender.description}
              </p>

              {/* Pros & Cons Card */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-50 border border-slate-100 p-6 rounded-xl mb-6">
                <div>
                  <h3 className="text-xs uppercase font-extrabold tracking-wider text-emerald-600 mb-3">Pros</h3>
                  <ul className="space-y-2 text-xs font-semibold text-slate-700">
                    {lender.pros.map((pro, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-emerald-500 font-extrabold">✓</span>
                        <span className="leading-snug">{pro}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="text-xs uppercase font-extrabold tracking-wider text-rose-600 mb-3">Cons</h3>
                  <ul className="space-y-2 text-xs font-semibold text-slate-700">
                    {lender.cons.map((con, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-rose-500 font-extrabold">✗</span>
                        <span className="leading-snug">{con}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Call to Action Button */}
              {lender.isPrimary ? (
                <a 
                  href={lender.ctaLink}
                  className="w-full inline-flex items-center justify-center px-6 h-12 rounded-xl bg-amber-600 text-white font-extrabold text-sm hover:bg-amber-700 transition-all shadow-md shadow-amber-600/15 text-center"
                >
                  {lender.ctaText} <span>&nbsp;→</span>
                </a>
              ) : (
                <a 
                  href={lender.ctaLink}
                  rel="nofollow"
                  className="w-full inline-flex items-center justify-center px-6 h-11 rounded-xl border border-slate-200 font-extrabold text-sm text-slate-700 bg-white hover:bg-slate-50 hover:text-slate-900 transition-colors text-center"
                >
                  {lender.ctaText}
                </a>
              )}
            </article>
          ))}
        </div>

        {/* Editorial Guide Section (Georgia Serif) */}
        <section className="pt-12 border-t-2 border-slate-200/80 space-y-8">
          <h2 className="text-2xl md:text-3xl lg:text-4xl font-extrabold tracking-tight text-slate-950 font-serif">
            The Ultimate Guide to Choosing a Mortgage Lender in New Hampshire
          </h2>
          
          <div className="font-serif text-slate-700 text-base md:text-lg leading-relaxed space-y-6">
            <p>
              New Hampshire’s real estate market has seen unprecedented shifts heading into 2026. With inventory remaining tight across major hubs like <strong>Manchester, Nashua, and Portsmouth</strong>, and the Seacoast becoming increasingly competitive, homebuyers are facing a landscape where speed and reliability are just as crucial as securing a low interest rate. 
              Whether you are a first-time homebuyer looking to leverage state assistance programs, or an experienced investor eyeing a multi-family property, selecting the right mortgage lender is the single most important financial decision you will make in this process.
            </p>

            <h3 className="text-xl md:text-2xl font-bold text-slate-900 font-sans pt-4">
              Understanding the NH Market Dynamics
            </h3>
            <p>
              Unlike national averages, the Granite State has a highly localized housing economy. Property taxes vary wildly from town to town, and rural properties may qualify for specialized USDA loans that suburban properties in Hillsborough County cannot access. A lender with a deep understanding of New Hampshire can help structure your loan to account for these local nuances, potentially saving you thousands in unnecessary escrow buffers or PMI (Private Mortgage Insurance) overcharges.
            </p>

            {/* In-text Editorial Callout Box linking to the new Blog */}
            <div className="glass-panel border-l-4 border-emerald-500 rounded-r-xl p-6 font-sans space-y-3 shadow-sm my-6">
              <span className="inline-flex px-2 py-0.5 rounded bg-emerald-50 border border-emerald-100 text-emerald-700 text-[10px] font-bold uppercase tracking-wider">
                First-Time Buyer Guide
              </span>
              <h4 className="text-base font-extrabold text-slate-950">
                Are you looking to qualify for down payment assistance?
              </h4>
              <p className="text-slate-600 font-medium text-xs md:text-sm leading-relaxed">
                The New Hampshire Housing Finance Authority provides substantial grants for qualified buyers. Read our full analysis:
              </p>
              <a 
                href="https://nh-mortgage-blog.onrender.com/blog/nhhfa-home-start-qualification-2026" 
                className="inline-flex items-center gap-1.5 text-xs font-extrabold text-blue-800 hover:underline"
              >
                How to Qualify for the NHHFA Home Start Program in 2026 <span>→</span>
              </a>
            </div>

            <h3 className="text-xl md:text-2xl font-bold text-slate-900 font-sans pt-4">
              What is the NHHFA (New Hampshire Housing Finance Authority)?
            </h3>
            <p>
              If you are a first-time homebuyer, or haven't owned a home in the last three years, you should strongly prioritize lenders who are approved to originate NH Housing loans. The NHHFA offers several vital programs:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-sm md:text-base">
              <li><strong>Home Start Program:</strong> Offers cash assistance for down payments and closing costs, structured as a forgivable loan over a short duration.</li>
              <li><strong>First-Time Homebuyer Tax Credit:</strong> A federal Mortgage Credit Certificate (MCC) that allows eligible NH buyers to claim up to $2,000 per year as a direct tax credit for the life of the loan.</li>
              <li><strong>Home Flex Plus:</strong> Government-insured loans (FHA, VA, Rural Development) paired with down payment assistance.</li>
            </ul>

            <h3 className="text-xl md:text-2xl font-bold text-slate-900 font-sans pt-4">
              Local Brokers vs. National Retail Lenders
            </h3>
            <p>
              You generally have three options when securing financing:
            </p>
            <ol className="list-decimal pl-6 space-y-4 text-sm md:text-base">
              <li>
                <strong>Independent Mortgage Brokers (Like our #1 pick):</strong> Brokers don't lend their own money. Instead, they shop your profile across dozens of wholesale lenders to find the lowest possible rate. Because they have lower overhead and access to wholesale pricing, brokers almost always beat retail banks on rate and closing costs.
              </li>
              <li>
                <strong>Direct Retail Lenders (Like Rocket Mortgage):</strong> These institutions lend their own funds. They offer highly polished digital experiences and fast pre-approvals, but because you are going direct to the source, you are paying retail margins.
              </li>
              <li>
                <strong>Local Credit Unions (Like St. Mary's Bank):</strong> Credit unions are member-owned and often hold loans in their own portfolio rather than selling them to Fannie Mae or Freddie Mac. This allows them to offer creative financing for unique properties (like a multi-family with mixed-use commercial space) that national lenders would immediately deny.
              </li>
            </ol>

            {/* Secondary Editorial Link Callout Box */}
            <div className="glass-panel border-l-4 border-blue-800 rounded-r-xl p-6 font-sans space-y-3 shadow-sm my-6">
              <span className="inline-flex px-2 py-0.5 rounded bg-blue-50 border border-blue-100 text-blue-800 text-[10px] font-bold uppercase tracking-wider">
                Closing Costs Guide
              </span>
              <h4 className="text-base font-extrabold text-slate-950">
                Don't get surprised by NH Transfer Taxes
              </h4>
              <p className="text-slate-600 font-medium text-xs md:text-sm leading-relaxed">
                New Hampshire levies a transfer tax on all sales. Learn what fees to expect and how to calculate them:
              </p>
              <a 
                href="https://nh-mortgage-blog.onrender.com/blog/estimated-closing-costs-nh" 
                className="inline-flex items-center gap-1.5 text-xs font-extrabold text-blue-800 hover:underline"
              >
                Granite State Closing Costs: Estimated Breakdown & Examples <span>→</span>
              </a>
            </div>

            <h3 className="text-xl md:text-2xl font-bold text-slate-900 font-sans pt-4">
              How to Compare Your Offers
            </h3>
            <p>
              Never look at the interest rate in a vacuum. A lender offering a 5.99% rate might be charging you $10,000 in upfront "discount points" to get that rate, while a lender offering 6.25% might be giving you a lender credit to cover your closing costs. Always request a <strong>Loan Estimate (LE)</strong> from at least three lenders. The LE is a standardized, federally mandated document that makes it mathematically impossible for lenders to hide junk fees. Compare the "Box A" origination charges across all three LEs to find the true cost of the loan.
            </p>
          </div>
        </section>

        {/* Disclaimer Footer */}
        <div className="mt-12 pt-8 border-t border-slate-200/80 text-slate-400 text-[10px] md:text-xs leading-relaxed text-center space-y-4">
          <p className="max-w-2xl mx-auto">
            <em><strong>Advertiser Disclosure:</strong> Many of the offers that appear on this site are from companies from which NH Financial Review receives compensation. This compensation may impact how and where products appear on this site (including, for example, the order in which they appear). However, this does not influence our evaluations. Our opinions are our own.</em>
          </p>
          <p className="font-semibold">
            © {new Date().getFullYear()} NH Financial Review. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
}
