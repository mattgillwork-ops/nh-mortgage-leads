import Link from "next/link";

const posts = [
  {
    slug: "nhhfa-home-start-qualification-2026",
    title: "How to Qualify for the NHHFA Home Start Program in 2026",
    excerpt: "Everything you need to know about qualifying for New Hampshire Housing's premier first-time homebuyer program, including income limits, credit scores, and down payment assistance.",
    date: "May 19, 2026",
    readTime: "6 min read",
    category: "First-Time Buyer",
    gradient: "from-slate-900 to-blue-900",
    pattern: (
      <svg className="absolute inset-0 w-full h-full opacity-10" fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <path d="M0 100 L50 20 L100 100 Z" stroke="currentColor" strokeWidth="2" />
        <path d="M20 100 L50 50 L80 100 Z" stroke="currentColor" strokeWidth="2" />
      </svg>
    )
  },
  {
    slug: "nh-mortgage-credit-score-requirements",
    title: "New Hampshire Mortgage Credit Score Requirements",
    excerpt: "What credit score do you actually need to buy a home in NH? Learn the requirements for FHA, USDA, VA, and Conventional loans in the Granite State.",
    date: "May 18, 2026",
    readTime: "5 min read",
    category: "Credit & Finance",
    gradient: "from-blue-900 to-emerald-900",
    pattern: (
      <svg className="absolute inset-0 w-full h-full opacity-10" fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <circle cx="50" cy="50" r="40" stroke="currentColor" strokeWidth="2" />
        <path d="M10 50 H90" stroke="currentColor" strokeWidth="1.5" />
        <path d="M50 10 V90" stroke="currentColor" strokeWidth="1.5" />
      </svg>
    )
  },
  {
    slug: "estimated-closing-costs-nh",
    title: "Granite State Closing Costs: Estimated Breakdown & Examples",
    excerpt: "Calculate your closing costs in NH. Understand transfer taxes, title fees, escrows, and how to minimize your out-of-pocket expenses when closing your loan.",
    date: "May 15, 2026",
    readTime: "7 min read",
    category: "Closing Costs",
    gradient: "from-indigo-950 to-amber-950",
    pattern: (
      <svg className="absolute inset-0 w-full h-full opacity-10" fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <rect x="15" y="15" width="70" height="70" rx="5" stroke="currentColor" strokeWidth="2" />
        <path d="M30 35 H70 M30 50 H70 M30 65 H50" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      </svg>
    )
  },
  {
    slug: "manchester-nh-mortgage-guide",
    title: "Navigating the Manchester, NH Housing Market: A Complete Guide",
    excerpt: "An in-depth guide to buying a home in the Queen City, covering North End vs. West Side, school districts, property taxes, and regional pre-approval options.",
    date: "May 20, 2026",
    readTime: "7 min read",
    category: "Local Guides",
    gradient: "from-slate-900 to-sky-900",
    pattern: (
      <svg className="absolute inset-0 w-full h-full opacity-10" fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <path d="M10 20 H90 V80 H10 Z" stroke="currentColor" strokeWidth="2" />
        <path d="M25 80 V50 M50 80 V35 M75 80 V60" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      </svg>
    )
  },
  {
    slug: "nashua-nh-homebuyer-handbook",
    title: "The Nashua Homebuyer Handbook: Commuting, Taxes, and Mortgages",
    excerpt: "A detailed analysis of Nashua's housing market, Boston commuter routes, Bicentennial school district, tax rates, and conventional loan guidelines.",
    date: "May 20, 2026",
    readTime: "6 min read",
    category: "Local Guides",
    gradient: "from-blue-900 to-indigo-950",
    pattern: (
      <svg className="absolute inset-0 w-full h-full opacity-10" fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <path d="M10 50 L30 20 H70 L90 50 L70 80 H30 Z" stroke="currentColor" strokeWidth="2" />
        <circle cx="50" cy="50" r="15" stroke="currentColor" strokeWidth="2" />
      </svg>
    )
  },
  {
    slug: "concord-nh-real-estate-guide",
    title: "Buying a Home in Concord, NH: The Capital City Mortgage Guide",
    excerpt: "Discover what makes Concord one of NH's most stable housing markets. Property tax rates, school details, and USDA/FHA financing programs.",
    date: "May 20, 2026",
    readTime: "6 min read",
    category: "Local Guides",
    gradient: "from-slate-900 to-emerald-950",
    pattern: (
      <svg className="absolute inset-0 w-full h-full opacity-10" fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <path d="M50 10 L90 40 V80 H10 V40 Z" stroke="currentColor" strokeWidth="2" />
        <path d="M35 80 V50 H65 V80" stroke="currentColor" strokeWidth="2" />
      </svg>
    )
  },
  {
    slug: "portsmouth-coastal-buyer-guide",
    title: "Portsmouth, NH Coastal Buyer Guide: Luxury Real Estate & Jumbo Loans",
    excerpt: "A guide to New Hampshire's premium coastal market. Historic South End, low property tax rates, and how to navigate jumbo mortgage financing.",
    date: "May 20, 2026",
    readTime: "8 min read",
    category: "Local Guides",
    gradient: "from-teal-950 to-blue-900",
    pattern: (
      <svg className="absolute inset-0 w-full h-full opacity-10" fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <path d="M10 80 C 30 70, 40 90, 60 80 C 80 70, 90 90, 100 80" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        <path d="M50 20 L25 60 H75 Z" stroke="currentColor" strokeWidth="2" />
        <line x1="50" y1="20" x2="50" y2="60" stroke="currentColor" strokeWidth="1.5" />
      </svg>
    )
  },
  {
    slug: "hanover-nh-homeowners-guide",
    title: "Hanover, NH Homeowners Guide: Dartmouth Area Financing & Real Estate",
    excerpt: "Navigating the Upper Valley's most exclusive market. Local school ratings, home values, and mortgage strategies for academic and medical professionals.",
    date: "May 20, 2026",
    readTime: "7 min read",
    category: "Local Guides",
    gradient: "from-emerald-950 to-stone-900",
    pattern: (
      <svg className="absolute inset-0 w-full h-full opacity-10" fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <rect x="20" y="20" width="60" height="60" rx="10" stroke="currentColor" strokeWidth="2" />
        <path d="M35 35 L65 65 M65 35 L35 65" stroke="currentColor" strokeWidth="2" />
      </svg>
    )
  }
];

export default function Home() {
  const featuredPost = posts[0];
  const recentPosts = posts.slice(1);

  return (
    <div className="flex-1 flex flex-col font-sans">
      {/* Premium Navbar */}
      <header className="sticky top-0 z-50 glass-panel border-b border-slate-200/80">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-navy-900 to-blue-800 flex items-center justify-center text-white font-extrabold text-lg shadow-md shadow-blue-900/10">
              NH
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight text-slate-900 block">NH Mortgage Journal</span>
              <span className="text-[10px] uppercase font-bold tracking-widest text-emerald-500 block -mt-1">Granite State Guide</span>
            </div>
          </div>
          
          <nav className="hidden md:flex items-center gap-8">
            <Link href="/" className="text-sm font-semibold text-slate-900 hover:text-blue-800 transition-colors">
              Home
            </Link>
            <Link href="/#articles" className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">
              Articles
            </Link>
            <a 
              href="https://nh-financial-review.onrender.com" 
              className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors"
            >
              Lender Reviews
            </a>
          </nav>

          <div>
            <a 
              href="https://nh-mortgage-leads.onrender.com/funnel?utm_source=nh-mortgage-blog&utm_medium=nav&utm_campaign=get-rates"
              className="inline-flex items-center justify-center px-5 h-11 rounded-lg bg-navy-900 text-white font-semibold text-sm hover:bg-slate-800 transition-colors shadow-sm"
            >
              Get Pre-Approved
            </a>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto px-6 py-12 w-full grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Main Content (Columns 1-8) */}
        <div className="lg:col-span-8 space-y-12">
          {/* Section: Featured Article */}
          <section className="space-y-6">
            <div className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
              <h2 className="text-xs uppercase font-extrabold tracking-widest text-slate-500">Featured Article</h2>
            </div>
            
            <article className="group relative overflow-hidden rounded-2xl border border-slate-200/80 bg-white hover-lift">
              {/* Graphic Banner */}
              <div className={`relative h-64 w-full bg-gradient-to-r ${featuredPost.gradient} flex items-center justify-center overflow-hidden text-white`}>
                {featuredPost.pattern}
                <div className="relative z-10 text-center px-8 max-w-lg">
                  <span className="inline-block px-3 py-1 rounded-full bg-white/10 text-xs font-semibold tracking-wide backdrop-blur-sm border border-white/20 mb-4">
                    {featuredPost.category}
                  </span>
                  <h3 className="text-3xl font-extrabold tracking-tight font-sans leading-tight">
                    {featuredPost.title}
                  </h3>
                </div>
              </div>

              {/* Text content */}
              <div className="p-8 space-y-4">
                <div className="flex items-center gap-4 text-xs font-semibold text-slate-400">
                  <span>{featuredPost.date}</span>
                  <span className="h-1 w-1 rounded-full bg-slate-300"></span>
                  <span>{featuredPost.readTime}</span>
                </div>
                <p className="text-slate-600 font-medium leading-relaxed text-base">
                  {featuredPost.excerpt}
                </p>
                <div className="pt-2">
                  <Link 
                    href={`/blog/${featuredPost.slug}`}
                    className="inline-flex items-center gap-2 text-sm font-extrabold text-blue-800 group-hover:text-blue-900"
                  >
                    Read Full Guide 
                    <span className="transition-transform group-hover:translate-x-1">→</span>
                  </Link>
                </div>
              </div>
            </article>
          </section>

          {/* Section: Recent Articles */}
          <section id="articles" className="space-y-6">
            <div className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-blue-800"></span>
              <h2 className="text-xs uppercase font-extrabold tracking-widest text-slate-500">Recent Guides</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {recentPosts.map((post) => (
                <article key={post.slug} className="group flex flex-col justify-between rounded-xl border border-slate-200/80 bg-white hover-lift">
                  <div>
                    {/* Graphic Thumbnail */}
                    <div className={`relative h-40 w-full bg-gradient-to-br ${post.gradient} rounded-t-xl flex items-center justify-center overflow-hidden text-white`}>
                      {post.pattern}
                      <span className="relative z-10 inline-block px-3 py-1 rounded-full bg-white/10 text-[10px] font-bold tracking-wide backdrop-blur-sm border border-white/20">
                        {post.category}
                      </span>
                    </div>

                    {/* Text Area */}
                    <div className="p-6 space-y-3">
                      <div className="flex items-center gap-3 text-[11px] font-semibold text-slate-400">
                        <span>{post.date}</span>
                        <span className="h-1 w-1 rounded-full bg-slate-300"></span>
                        <span>{post.readTime}</span>
                      </div>
                      <h3 className="font-extrabold text-lg tracking-tight text-slate-900 group-hover:text-blue-800 transition-colors leading-snug">
                        {post.title}
                      </h3>
                      <p className="text-slate-500 font-medium text-xs leading-relaxed line-clamp-3">
                        {post.excerpt}
                      </p>
                    </div>
                  </div>

                  <div className="px-6 pb-6 pt-2">
                    <Link 
                      href={`/blog/${post.slug}`}
                      className="inline-flex items-center gap-1.5 text-xs font-extrabold text-blue-800"
                    >
                      Read Article <span>→</span>
                    </Link>
                  </div>
                </article>
              ))}
            </div>
          </section>
        </div>

        {/* Sidebar (Columns 9-12) */}
        <aside className="lg:col-span-4 space-y-8">
          {/* Glassmorphic Conversion Card */}
          <div className="glass-panel rounded-2xl p-8 border border-slate-200/85 relative overflow-hidden shadow-lg shadow-slate-100/50">
            {/* Design accents */}
            <div className="absolute -top-12 -right-12 w-28 h-28 rounded-full bg-blue-500/10 blur-xl"></div>
            <div className="absolute -bottom-12 -left-12 w-28 h-28 rounded-full bg-emerald-500/10 blur-xl"></div>
            
            <div className="relative z-10 space-y-6">
              <div className="inline-flex items-center justify-center px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 text-[10px] font-bold tracking-widest uppercase">
                Rates Update
              </div>
              
              <div className="space-y-2">
                <h3 className="text-2xl font-extrabold tracking-tight text-slate-900 leading-tight">
                  NH Mortgage rates are shifting.
                </h3>
                <p className="text-slate-600 font-medium text-sm leading-relaxed">
                  Are you planning to buy a home in Manchester, Nashua, or Portsmouth? Check your custom mortgage rate in under 2 minutes.
                </p>
              </div>

              {/* Rate Stats */}
              <div className="py-2 border-y border-slate-200/50 grid grid-cols-2 gap-4">
                <div>
                  <span className="block text-[10px] uppercase font-bold text-slate-400">30-Yr Fixed (NH)</span>
                  <span className="block text-xl font-extrabold text-slate-800">6.45%*</span>
                </div>
                <div>
                  <span className="block text-[10px] uppercase font-bold text-slate-400">15-Yr Fixed (NH)</span>
                  <span className="block text-xl font-extrabold text-slate-800">5.75%*</span>
                </div>
              </div>

              <a 
                href="https://nh-mortgage-leads.onrender.com/funnel?utm_source=nh-mortgage-blog&utm_medium=sidebar&utm_campaign=rates-card"
                className="w-full inline-flex items-center justify-center px-5 h-12 rounded-xl bg-amber-600 text-white font-extrabold text-sm hover:bg-amber-700 transition-all shadow-md shadow-amber-600/15 hover:shadow-amber-600/25 text-center"
              >
                Compare Live Rates <span>&nbsp;→</span>
              </a>

              <p className="text-[10px] text-slate-400 font-medium text-center">
                *Estimated rates based on regional averages. Rates vary by credit score & down payment.
              </p>
            </div>
          </div>

          {/* NH Mortgage List Site Promo Card */}
          <div className="rounded-2xl border border-slate-200/80 bg-white p-8 space-y-6">
            <div className="space-y-2">
              <h4 className="font-extrabold text-lg text-slate-900 leading-snug">
                Compare NH Lenders
              </h4>
              <p className="text-slate-500 font-medium text-xs leading-relaxed">
                Don't settle for the first quote. See our unbiased review of the Top 10 mortgage lenders in New Hampshire.
              </p>
            </div>
            
            <a 
              href="https://nh-financial-review.onrender.com?utm_source=nh-mortgage-blog&utm_medium=sidebar&utm_campaign=lender-review-promo"
              className="w-full inline-flex items-center justify-center px-4 h-10 rounded-lg border border-slate-200 font-bold text-xs text-slate-700 hover:bg-slate-50 hover:text-slate-900 transition-colors text-center"
            >
              Read Lender Reviews
            </a>
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
              <a href="https://nh-mortgage-leads.onrender.com/funnel?utm_source=nh-mortgage-blog&utm_medium=footer&utm_campaign=get-preapproved" className="hover:text-slate-800">Get Pre-Approved</a>
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
