import { NextRequest, NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const tierId = body?.tierId as string | undefined;
    const billingCycle = (body?.billing_cycle as 'monthly' | 'yearly' | undefined) || 'monthly';

    if (!tierId) {
      return NextResponse.json({ ok: false, error: 'tierId required' }, { status: 400 });
    }

    // TODO: Integrate with backend billing service if available.
    // For now, acknowledge subscription intent for analytics/audit.
    console.log('[tiers/subscribe] intent', { tierId, billingCycle });

    return NextResponse.json({ ok: true, tierId, billingCycle }, { status: 200 });
  } catch (e: unknown) {
    const message = e instanceof Error ? e.message : 'invalid request';
    return NextResponse.json({ ok: false, error: message }, { status: 400 });
  }
}
