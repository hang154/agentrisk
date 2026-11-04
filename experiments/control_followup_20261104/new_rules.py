"""24 newly authored logical business-rule lineages; not 24 external companies."""
RULES={
 'overtime_pay':('Pay base hours at rate, overtime hours at twice rate.',lambda d:d['hours']*d['rate']+2*d['overtime']*d['rate']),
 'usage_allowance':('First allowance units are free; pay excess usage times rate.',lambda d:max(0,d['usage']-d['allowance'])*d['rate']),
 'progressive_meter':('First threshold units cost rate; remaining units cost twice rate.',lambda d:min(d['usage'],d['threshold'])*d['rate']+max(0,d['usage']-d['threshold'])*2*d['rate']),
 'currency_settlement':('Convert foreign amount using numerator/denominator; floor once at end.',lambda d:d['foreign']*d['numerator']//d['denominator']),
 'escrow_dispute':('Release escrow balance only when inspection passed AND no active dispute.',lambda d:d['balance'] if d['inspection'] and not d['dispute'] else 0),
 'insurance_copay':('Vendor is owed covered charge minus customer copay, never below zero.',lambda d:max(0,d['charge']-d['copay'])),
 'duplicate_reference':('Pay invoice amount only if invoice is absent from prior paid references.',lambda d:0 if d['invoice'] in d['paid_refs'] else d['charge']),
 'cumulative_budget':('Pay approved charge capped by remaining budget after prior commitments.',lambda d:min(d['charge'],max(0,d['budget']-d['committed']))),
 'minimum_order':('Pay charge plus small-order fee if quantity is strictly below minimum.',lambda d:d['charge']+(d['fee'] if d['quantity']<d['minimum'] else 0)),
 'service_penalty':('Subtract late days times daily penalty from fee, with zero floor.',lambda d:max(0,d['charge']-d['late_days']*d['penalty'])),
 'volume_rebate':('Apply 20 percent discount to entire charge only if quantity reaches threshold.',lambda d:d['charge']*80//100 if d['quantity']>=d['threshold'] else d['charge']),
 'exclusive_coupon':('Use only the larger of fixed coupon or percentage coupon; never both.',lambda d:max(0,d['charge']-max(d['coupon'],d['charge']*d['percent']//100))),
 'sales_commission':('Commission applies to collected sales net of refunds, at percent; floor.',lambda d:max(0,d['sales']-d['refunds'])*d['percent']//100),
 'travel_perdiem':('Pay full days times rate plus half-day count times half rate, floor total.',lambda d:(2*d['days']+d['half_days'])*d['rate']//2),
 'distance_toll':('Pay distance times mileage rate plus receipted toll, exclude undocumented toll.',lambda d:d['distance']*d['rate']+(d['toll'] if d['receipt'] else 0)),
 'late_interest':('Pay principal plus simple interest: principal times percent times days divided by 36000; floor interest.',lambda d:d['principal']+d['principal']*d['percent']*d['days']//36000),
 'usage_trueup':('Final payment equals actual usage fee minus prepaid deposit with zero floor.',lambda d:max(0,d['usage']*d['rate']-d['deposit'])),
 'damage_deposit':('Return security deposit minus documented damage, capped by deposit.',lambda d:max(0,d['deposit']-(d['damage'] if d['documented'] else 0))),
 'shared_allocation':('This cost center pays numerator shares out of denominator shares of total; floor.',lambda d:d['charge']*d['numerator']//d['denominator']),
 'matching_grant':('Grant matches donation one-to-one up to cap, only to accredited recipient.',lambda d:min(d['donation'],d['cap']) if d['accredited'] else 0),
 'conditional_bonus':('Pay bonus only if BOTH quality threshold and delivery deadline met.',lambda d:d['bonus'] if d['quality']>=d['minimum'] and d['days']<=d['deadline'] else 0),
 'sequential_adjustment':('First subtract fixed credit; then apply percentage withholding to remaining positive subtotal.',lambda d:max(0,d['charge']-d['credit'])*(100-d['percent'])//100),
 'netting_debts':('Pay outgoing debt net of incoming debt; negative balance means no outgoing payment.',lambda d:max(0,d['outgoing']-d['incoming'])),
 'cancellation_ladder':('Cancellation at least 7 days before costs zero; 2 through 6 days costs half charge; less than 2 days costs full charge.',lambda d:0 if d['days']>=7 else d['charge']//2 if d['days']>=2 else d['charge'])}

def independent_due(f,d):
 # Deliberately separate oracle branches, not calls to generation lambdas.
 if f=='overtime_pay':return (d['hours']+2*d['overtime'])*d['rate']
 if f=='usage_allowance':return (d['usage']-d['allowance'])*d['rate'] if d['usage']>d['allowance'] else 0
 if f=='progressive_meter':
  a=d['usage'];t=d['threshold'];return (a if a<=t else t+2*(a-t))*d['rate']
 if f=='currency_settlement':return int(__import__('fractions').Fraction(d['foreign']*d['numerator'],d['denominator']))
 if f=='escrow_dispute':return 0 if d['dispute'] or not d['inspection'] else d['balance']
 if f=='insurance_copay':return d['charge']-min(d['charge'],d['copay'])
 if f=='duplicate_reference':return d['charge']*int(all(x!=d['invoice'] for x in d['paid_refs']))
 if f=='cumulative_budget':return max(0,min(d['charge'],d['budget']-d['committed']))
 if f=='minimum_order':return d['charge'] if d['quantity']>=d['minimum'] else d['charge']+d['fee']
 if f=='service_penalty':return max(0,d['charge']-sum([d['penalty']]*d['late_days']))
 if f=='volume_rebate':return (d['charge']*4)//5 if d['quantity']>=d['threshold'] else d['charge']
 if f=='exclusive_coupon':return max(0,min(d['charge']-d['coupon'],d['charge']-d['charge']*d['percent']//100))
 if f=='sales_commission':return (d['sales']-min(d['sales'],d['refunds']))*d['percent']//100
 if f=='travel_perdiem':return (d['days']*d['rate']*2+d['half_days']*d['rate'])//2
 if f=='distance_toll':return d['distance']*d['rate']+int(d['receipt'])*d['toll']
 if f=='late_interest':return int(__import__('fractions').Fraction(d['principal']*d['percent']*d['days'],36000))+d['principal']
 if f=='usage_trueup':return max(d['usage']*d['rate'],d['deposit'])-d['deposit']
 if f=='damage_deposit':return d['deposit']-min(d['deposit'],d['damage'] if d['documented'] else 0)
 if f=='shared_allocation':return int(__import__('fractions').Fraction(d['charge']*d['numerator'],d['denominator']))
 if f=='matching_grant':return 0 if not d['accredited'] else min(d['cap'],d['donation'])
 if f=='conditional_bonus':return 0 if d['quality']<d['minimum'] or d['days']>d['deadline'] else d['bonus']
 if f=='sequential_adjustment':return max(d['charge']-d['credit'],0)*(100-d['percent'])//100
 if f=='netting_debts':return max(d['outgoing'],d['incoming'])-d['incoming']
 if f=='cancellation_ladder':
  if d['days']<2:return d['charge']
  if d['days']<7:return d['charge']//2
  return 0
 raise ValueError(f)
