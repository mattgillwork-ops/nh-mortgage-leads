import { NextResponse } from 'next/server';
import { AFFILIATE_LINKS } from '@/lib/affiliates';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ lenderId: string }> }
) {
  const resolvedParams = await params;
  const lenderId = resolvedParams.lenderId;
  const targetUrl = AFFILIATE_LINKS[lenderId];

  if (!targetUrl) {
    // Fallback to homepage if lender ID is unknown
    return NextResponse.redirect(new URL('/', request.url));
  }

  // Optional: Add analytics logging here in the future
  // console.log(`[AFFILIATE CLICK] Routing to ${lenderId}`);

  // Issue a 302 Temporary Redirect to the affiliate URL with noindex, nofollow headers
  // 302 is preferred for affiliate links so browsers don't cache it permanently
  return new NextResponse(null, {
    status: 302,
    headers: {
      'Location': targetUrl,
      'X-Robots-Tag': 'noindex, nofollow',
    },
  });
}
