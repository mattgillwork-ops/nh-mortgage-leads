import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/private/', '/admin/', '?session_id='],
      crawlDelay: 10,
    },
    sitemap: 'https://nh-mortgage-blog.onrender.com/sitemap.xml',
  };
}
