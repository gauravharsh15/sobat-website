# The five launch posts. Body HTML only; build.py wraps each in the page.
TOMTOM = "https://www.downtoearth.org.in/urbanisation/bengaluru-kolkata-among-worlds-slowest-cities-as-india-ranks-high-on-congestion-index"
WRI = "https://vajiramandravi.com/current-affairs/co2-emissions-from-transport-sector-could-be-slashed-up-to-71-by-2050-study/"

POSTS = [
dict(
slug="share-cab-with-strangers-safely",
title="How to Share a Cab with Strangers Safely | Sobat",
h1="How to share a cab with strangers safely",
eyebrow="Safety",
desc="Sharing a cab with people you haven't met? 15 practical tips: where to meet, what to check before you get in, keeping your number private and when to leave.",
card="Where to meet, what to check before you get in, how to keep your number private, and when to walk away.",
lede="Sharing a cab with people going your way cuts the fare and the traffic. It also means riding with people you haven't met. Staying safe comes down to a few habits: meet in public, check the cab, keep your details private, and leave if anything feels off. Here's a practical checklist.",
related=["how-to-split-cab-fare", "is-carpooling-legal-in-india", "outstation-cab-sharing"],
body="""
<h2>Before you agree to share</h2>
<ol>
  <li><strong>Judge the ride first.</strong> Where does it start and end, when does it leave, and how are its riders rated? On Sobat you see exactly that before joining: the route, the time, free seats and the riders' average rating. Names and photos appear only once you're in.</li>
  <li><strong>Prefer riders with a track record.</strong> Ratings after every ride make no-shows and bad behaviour visible. A ride whose riders are well rated is a safer first choice than one nobody has rated yet.</li>
  <li><strong>Choose women-only rides if you'd rather.</strong> On Sobat, women can pick rides where every rider is a woman. It's enforced on Sobat's servers, not just in the app, so nobody can slip in by changing a setting.</li>
  <li><strong>Tell someone your plan.</strong> Send a friend or family member where you're meeting, where you're going and when you expect to arrive.</li>
</ol>

<h2>At the meeting point</h2>
<ol start="5">
  <li><strong>Meet somewhere public and busy.</strong> A metro exit, a mall entrance, an office gate with a guard. Never a quiet lane, and never someone's home.</li>
  <li><strong>Arrive a few minutes early.</strong> You'll see the others arrive instead of walking up to a waiting group. On Sobat, tap "I'm here" so everyone knows who has arrived.</li>
  <li><strong>Book through a regular ride app, or take a metered auto.</strong> The trip is then on record and the driver is registered with the platform. Don't get into a private car because someone in the group "knows a driver".</li>
  <li><strong>Check the cab before you get in.</strong> The number plate, the car and the driver's photo should match what the booking app shows. If they don't, don't get in.</li>
</ol>

<h2>During the ride</h2>
<ol start="9">
  <li><strong>Share the trip live.</strong> Ride apps like Ola and Uber let you share a live link to the trip. Whoever books should send it to the group, and you can forward it to someone you trust.</li>
  <li><strong>Keep your phone number private.</strong> Coordinate in the ride's chat instead. Sobat's chat has quick replies ("Running 2 min late", "I'm at the pickup") and never shows anyone's number.</li>
  <li><strong>Know your emergency options.</strong> 112 is India's single emergency number, and the big ride apps have an emergency button on the trip screen. Find it before you need it.</li>
  <li><strong>Sit where you're comfortable.</strong> If you'd rather not sit next to someone, ask to swap. Nobody should mind.</li>
</ol>

<h2>After the ride</h2>
<ol start="13">
  <li><strong>Settle the fare straight away</strong> by UPI, before everyone walks off. No "I'll send it later", and no reason to swap numbers. Our guide to <a href="/blog/how-to-split-cab-fare/">splitting a cab fare fairly</a> shows how.</li>
  <li><strong>Rate your co-riders honestly.</strong> It's how the next person knows who shows up on time and who doesn't.</li>
  <li><strong>Report or block anyone who made you uncomfortable.</strong> On Sobat, blocking someone means you'll never be matched with them again.</li>
</ol>

<h2>When to walk away</h2>
<p>You never owe anyone a shared ride. Leave if:</p>
<ul>
  <li>the meeting point moves somewhere private or poorly lit;</li>
  <li>someone presses for your phone number, or wants to skip the app and "just go";</li>
  <li>the cab that turns up doesn't match the booking;</li>
  <li>anything simply feels wrong.</li>
</ul>
<p>On Sobat, leaving a ride takes one tap, and the others are told so nobody waits for you.</p>

<h2>How Sobat is built for this</h2>
<p>Sobat helps people going the same way find each other, meet at one public pickup point and book one regular cab. Before you join, you see rides, not people. Women can choose women-only rides. Chat works without phone numbers, riders rate each other after every trip, and anyone can be reported or blocked.</p>
<p>Sobat doesn't drive, track or book the cab itself. For the ride, use your ride app's trip sharing and safety features.</p>
"""),

dict(
slug="how-to-split-cab-fare",
title="How to Split a Cab Fare Fairly, With Examples | Sobat",
h1="How to split a cab fare fairly",
eyebrow="Fares",
desc="Fair ways to split a shared cab fare: equal shares, by distance when drops differ, tolls and waiting charges, and settling by UPI. Worked examples in rupees.",
card="Equal shares, splitting by distance when people get off early, tolls and waiting, and settling up by UPI.",
lede="The simplest fair split is equal shares: the fare divided by the number of people. When people get off at different places, split by distance instead. Agree on the method before the ride, let one person pay the driver, and settle by UPI as soon as you get out. Worked examples below.",
related=["outstation-cab-sharing", "save-money-office-commute-cab", "share-cab-with-strangers-safely"],
body="""
<h2>Agree on three things before you get in</h2>
<ul>
  <li><strong>Who books and pays the driver.</strong> One person books on their ride app and pays at the end; everyone else pays them back.</li>
  <li><strong>How you'll split.</strong> Equal shares, or by distance if people get off at different places.</li>
  <li><strong>What happens with extras:</strong> tolls, waiting time and detours (more on these below).</li>
</ul>
<p>Thirty seconds of agreement at the pickup point saves an awkward conversation at the drop.</p>

<h2>Method 1: equal shares</h2>
<p>When everyone starts and ends at roughly the same place, split the fare equally per person. If someone brings a friend, they pay two shares.</p>
<div class="table-wrap">
<table class="table">
  <caption>Example: a ₹420 cab</caption>
  <thead><tr><th scope="col">Riders</th><th scope="col">Each pays</th><th scope="col">Each saves</th></tr></thead>
  <tbody>
    <tr><td>1</td><td>₹420</td><td>–</td></tr>
    <tr><td>2</td><td>₹210</td><td>₹210</td></tr>
    <tr><td>3</td><td>₹140</td><td>₹280</td></tr>
    <tr><td>4</td><td>₹105</td><td>₹315</td></tr>
  </tbody>
</table>
</div>
<p>Round each share to the nearest ₹5 and don't argue over a few rupees.</p>

<h2>Method 2: by distance, when drops differ</h2>
<p>If one person gets off early, an equal split makes them pay for kilometres they never rode. There are two fair ways to fix that.</p>

<h3>Pay in proportion to the distance you ride</h3>
<p>Add up everyone's kilometres; each person pays their kilometres' share of the fare.</p>
<div class="callout">
  <p><strong>Example.</strong> A ₹600 cab covers 24 km. Asha rides all 24 km, Ben gets off after 16 km and Chirag after 8 km. Together they ride 24 + 16 + 8 = 48 km.</p>
  <ul>
    <li>Asha: 24 of 48 km, half → <strong>₹300</strong></li>
    <li>Ben: 16 of 48 km, a third → <strong>₹200</strong></li>
    <li>Chirag: 8 of 48 km, a sixth → <strong>₹100</strong></li>
  </ul>
</div>

<h3>Split each stretch among whoever is aboard</h3>
<p>Divide the trip into stretches between drops, and share each stretch's cost among the people in the cab for it. With the same ₹600 cab, each 8 km stretch costs ₹200: the first is split three ways, the second two ways, and the last is Asha's alone. Asha pays about ₹367, Ben about ₹167 and Chirag about ₹67.</p>
<p>This second method charges the last rider more, because they ride the final stretch alone. Both are fair; pick one before the ride starts.</p>

<h2>Tolls, waiting, detours and surge</h2>
<ul>
  <li><strong>Tolls:</strong> split among the people in the cab when it crosses the toll.</li>
  <li><strong>Waiting charges:</strong> if the cab waited because one person was late, that person covers it.</li>
  <li><strong>Detours:</strong> if the cab goes out of its way for one person's drop, that person pays the extra.</li>
  <li><strong>Surge pricing:</strong> shared equally. Whoever booked would have seen the same price.</li>
</ul>

<h2>Settle up by UPI before you walk away</h2>
<p>The booker pays the driver, in the app or in cash. Everyone else sends their share by UPI right there: scan the booker's QR code or send it to their UPI ID. UPI payments between people are free and instant, and some UPI apps have a split-bill feature for groups.</p>
<p>Don't leave it for later. People who share a cab once rarely see each other again, and "I'll send it tonight" is how fares go unpaid.</p>

<h2>Who should book?</h2>
<p>Anyone in the group can. A good rule: whoever reaches the pickup point first books, so the cab is on its way while the others arrive. Say in the group chat who's booking, so two people don't book two cabs.</p>

<h2>How Sobat handles the split</h2>
<p>Sobat starts every ride with an equal split by head. Once someone enters what the cab cost, everyone sees their share in rupees. Anyone can change their own share, for example if they get off early, and the chat shows the change so it's never silent. On <a href="/blog/outstation-cab-sharing/">outstation rides</a>, Sobat splits by the distance each person rides.</p>
<p>Sobat never handles the money: you settle with each other directly.</p>
"""),

dict(
slug="outstation-cab-sharing",
title="Outstation Cab Sharing: A Complete Guide | Sobat",
h1="Outstation cab sharing: a complete guide",
eyebrow="Outstation",
desc="How outstation cab sharing works: finding people whose route passes near you, pickups along the way, splitting the fare by distance, tolls and luggage.",
card="Finding people whose route passes near you, pickups along the way, and splitting the fare by distance.",
lede="An outstation cab is one of the most comfortable ways to travel between cities, and one of the priciest when you go alone. Shared with people heading the same way, it costs each of you a fraction of the fare. You don't even need to start at the same place: the cab can pick people up along its route.",
related=["how-to-split-cab-fare", "share-cab-with-strangers-safely", "is-carpooling-legal-in-india"],
body="""
<h2>How it works</h2>
<ol>
  <li><strong>Someone starts the trip:</strong> where from, where to, and when.</li>
  <li><strong>Others whose trip lies along the same road join.</strong> They don't need to start at the same place. Someone across town near the highway fits, and so does someone getting off at a town on the way.</li>
  <li><strong>One person books an outstation cab for the whole route</strong>, on a ride app or with a local taxi operator.</li>
  <li><strong>The cab picks everyone up in order along the road</strong>, and drops them in order.</li>
  <li><strong>Everyone pays for the distance they ride.</strong></li>
</ol>

<h2>Finding people going your way</h2>
<p>For long trips, matching start and end points isn't enough. Two people heading to the same hill station may start 20 km apart, but if the highway passes near both of them, one cab can carry both.</p>
<p>On Sobat, choose <strong>Outstation</strong> when you search. You'll see rides whose route passes near your pickup and then your drop, even if they start somewhere else. For each ride, Sobat shows when the cab reaches you, how far it would go out of its way to pick you up, and how many kilometres you'd share. Trips of 40 km or more are treated as outstation automatically, and you can switch.</p>

<h2>Pickups along the way</h2>
<ul>
  <li><strong>Choose stops on the main road:</strong> a fuel station, a well-known landmark or a bus stop by the highway. Avoid detours into narrow lanes; every extra kilometre is paid for.</li>
  <li><strong>Agree on times, and be early.</strong> If the cab reaches you around 7:40, be there by 7:30. A cab can't wait long on a busy highway.</li>
  <li><strong>Share your location in the chat</strong> as the cab gets close, so the driver doesn't miss you.</li>
</ul>

<h2>Splitting the fare by distance</h2>
<p>Everyone pays in proportion to the kilometres they ride. Here's how that works with example numbers.</p>
<div class="callout">
  <p><strong>Example.</strong> A 150 km trip costs ₹3,600. Meera rides the whole way (150 km). Arjun joins 30 km in and rides to the end (120 km). Sana rides from the start and gets off at a town 90 km along (90 km). Together: 150 + 120 + 90 = 360 km.</p>
  <ul>
    <li>Meera: 150 of 360 km → <strong>₹1,500</strong></li>
    <li>Arjun: 120 of 360 km → <strong>₹1,200</strong></li>
    <li>Sana: 90 of 360 km → <strong>₹900</strong></li>
  </ul>
  <p>Alone, Meera would have paid ₹3,600.</p>
</div>
<p>For other ways to split, see <a href="/blog/how-to-split-cab-fare/">how to split a cab fare fairly</a>.</p>

<h2>Check these costs before you book</h2>
<ul>
  <li><strong>Tolls, state entry taxes and parking:</strong> on many outstation bookings these are extra. Check what the quoted fare includes.</li>
  <li><strong>Driver allowance and night charges:</strong> some fares add these for late-night or overnight trips.</li>
  <li><strong>One way or round trip:</strong> they're priced differently. If nobody is coming back the same day, book one way.</li>
  <li><strong>Waiting time:</strong> agree how long the cab will wait at each pickup.</li>
</ul>

<h2>Luggage, breaks and comfort</h2>
<ul>
  <li><strong>Say how many bags you have when you join.</strong> A sedan's boot fills up fast with four people's luggage; if everyone has a suitcase, book an SUV.</li>
  <li><strong>Agree on stops.</strong> On a long drive, plan one break for food and toilets so nobody has to ask.</li>
  <li><strong>Front seat:</strong> give it to whoever gets carsick.</li>
</ul>

<h2>Stay safe on longer trips</h2>
<p>The same habits apply as in town, with a little more planning: meet at public points, share the trip's live link with someone at home, and keep your phone charged. Our guide to <a href="/blog/share-cab-with-strangers-safely/">sharing a cab with strangers safely</a> has the full checklist.</p>

<h2>How Sobat helps</h2>
<p>Outstation rides on Sobat follow the actual road. The ride lists every stop in road order and draws the route, so everyone knows when the cab reaches them. The fare is split by distance automatically, and anyone can adjust their own share. You still book the cab yourselves, and Sobat never handles the money.</p>
"""),

dict(
slug="save-money-office-commute-cab",
title="How Much Does Sharing Your Office Cab Save? | Sobat",
h1="How much does sharing your office cab actually save?",
eyebrow="Commute",
desc="Worked numbers for a daily office commute: what a shared cab saves each month in rupees and in CO₂, a formula for your own commute, and how to start sharing it.",
card="Worked numbers for a daily commute: the rupees and the CO₂ a shared cab saves each month.",
lede="If you take a cab to work, sharing it with two colleagues going the same way cuts your fare to about a third. Over a month of working days, that's often thousands of rupees. It also takes two cabs off the road on every trip. Here's the maths, with example numbers you can swap for your own.",
related=["how-to-split-cab-fare", "is-carpooling-legal-in-india", "share-cab-with-strangers-safely"],
body=f"""
<h2>The money, worked out</h2>
<p>Take an example commute: a cab costs ₹350 each way, and you work 22 days a month. That's 44 trips.</p>
<div class="table-wrap">
<table class="table">
  <caption>Example: 44 trips a month at ₹350 a trip</caption>
  <thead><tr><th scope="col">Sharing with</th><th scope="col">You pay a month</th><th scope="col">You save a month</th></tr></thead>
  <tbody>
    <tr><td>Nobody</td><td>₹15,400</td><td>–</td></tr>
    <tr><td>1 other person</td><td>₹7,700</td><td>₹7,700</td></tr>
    <tr><td>2 others</td><td>₹5,133</td><td>₹10,267</td></tr>
    <tr><td>3 others</td><td>₹3,850</td><td>₹11,550</td></tr>
  </tbody>
</table>
</div>
<p>For your own commute: <strong>monthly saving = fare per trip × trips a month × (1 − 1 ÷ number of riders)</strong>.</p>
<p>Real life is a little messier. Some days you'll ride alone, and a full cab sometimes needs a bigger car. Even so, sharing only on the days it works out adds up quickly.</p>

<h2>The CO₂, worked out</h2>
<p>When three people share one cab instead of taking three, two cabs stay off the road for the whole trip. Sobat counts <strong>120 g of CO₂ for every kilometre a cab drives</strong>. That's close to what India's fuel-efficiency rules allow new cars on average, and on the conservative side, since stop-and-go city traffic usually burns more.</p>
<div class="callout">
  <p><strong>Example.</strong> A 15 km commute by road, shared by three people:</p>
  <ul>
    <li>Each trip avoids 2 cabs × 15 km × 0.12 kg = <strong>3.6 kg of CO₂</strong></li>
    <li>Over 44 trips a month: about <strong>158 kg</strong> for the group, roughly <strong>53 kg each</strong></li>
    <li>A tree takes up roughly 22 kg of CO₂ a year, so each person's month of sharing is like 2.4 trees working for a whole year</li>
  </ul>
</div>

<h2>The traffic</h2>
<p>Cabs carrying one person are a big part of why commutes crawl. Two of the world's five most congested cities in 2025 were in India, according to the <a href="{TOMTOM}" rel="noopener" target="_blank">TomTom Traffic Index</a>, and road vehicles produce about 90% of India's transport CO₂, according to <a href="{WRI}" rel="noopener" target="_blank">WRI India</a>. Every shared cab is one or two cars fewer at the signal.</p>

<h2>How to start sharing your commute</h2>
<ol>
  <li><strong>Find people on your route:</strong> colleagues in your building, neighbours in your society, your office's WhatsApp groups.</li>
  <li><strong>Pick one meeting point</strong> everyone can walk to in a few minutes.</li>
  <li><strong>Fix a time window</strong>, say 9:00 to 9:15, so nobody waits long.</li>
  <li><strong>Agree how you'll split</strong> before the first ride. Our <a href="/blog/how-to-split-cab-fare/">fare-splitting guide</a> has the options.</li>
  <li><strong>Put it on Sobat.</strong> Start a ride for your time and share its link in your group; anyone searching your route sees it too. You choose how far you'll walk to meet: 5, 10, 15 or 20 minutes.</li>
</ol>
<p>Sobat shows the CO₂ each shared ride saved and keeps a running total for you.</p>
"""),
]
