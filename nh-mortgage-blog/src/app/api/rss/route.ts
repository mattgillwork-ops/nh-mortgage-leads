import { newArticles } from "../../blog/data/newArticles";

export async function GET() {
  const site_url = "https://nh-mortgage-blog.onrender.com";

  let rss = `<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>New England Mortgage Journal</title>
  <link>${site_url}</link>
  <description>The latest updates, grants, and wholesale rate analysis for New England homebuyers.</description>
`;

  // We loop through the articles to create the feed
  for (const [slug, data] of Object.entries(newArticles)) {
    const articleUrl = `${site_url}/blog/${slug}`;
    const title = data.content.title;

    // Build the GMB optimized description
    let descriptionText = `🚨 New Update: ${title}\n\n`;
    
    if (data.takeaways && data.takeaways.length > 0) {
      data.takeaways.forEach((t) => {
        descriptionText += `✅ ${t}\n`;
      });
    } else {
      descriptionText += `${data.content.excerpt}\n`;
    }
    
    descriptionText += `\nTap 'Learn More' to read the full guide and check your eligibility.`;

    rss += `
  <item>
    <title><![CDATA[${title}]]></title>
    <link>${articleUrl}</link>
    <description><![CDATA[${descriptionText}]]></description>
    <pubDate>${new Date(data.content.date).toUTCString()}</pubDate>
    <guid>${articleUrl}</guid>
  </item>`;
  }

  rss += `
</channel>
</rss>`;

  return new Response(rss, {
    headers: {
      "Content-Type": "application/xml",
    },
  });
}
