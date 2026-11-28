// Strict offline transport for child-process collector acceptance. Never delegates to real fetch.
import fs from 'node:fs';
import net from 'node:net';
import tls from 'node:tls';
import http from 'node:http';
import https from 'node:https';
const deny = () => { throw new Error('Unexpected network access in analytics fixture'); };
net.Socket.prototype.connect = deny;
tls.connect = deny;
http.request = https.request = http.get = https.get = deny;
const channels = {owb:'UC_esArsDKd3GJvOkeO0DUog', hos:'UCXp7HkBIl1LgaznXuZHJyRg', ww2:'UC0000000000000000000000'};
const videos = {owb:'fixtureowb1', hos:'fixturehos1', ww2:'fixtureww21'};
const response = (body, status=200) => new Response(JSON.stringify(body), {status});
globalThis.fetch = async (input, init={}) => {
  const url = new URL(String(input));
  fs.appendFileSync(process.env.FIXTURE_REQUEST_LOG, JSON.stringify({host:url.hostname,path:url.pathname})+'\n');
  if(url.href === 'https://oauth2.googleapis.com/token') {
    const slug = new URLSearchParams(init.body).get('refresh_token');
    if(!channels[slug]) throw new Error('Unexpected fixture identity');
    return response({access_token:slug,expires_in:3600});
  }
  const slug = String(init.headers?.Authorization).replace('Bearer ','');
  if(!channels[slug]) throw new Error('Unexpected fixture identity');
  if(url.hostname==='www.googleapis.com') {
    if(slug===process.env.FIXTURE_FAIL_CHANNEL) return response({error:{message:'fixture failure'}},400);
    if(url.pathname==='/youtube/v3/channels') return response({items:[{id:channels[slug],snippet:{publishedAt:'2026-01-01T00:00:00Z'},statistics:{subscriberCount:'12',viewCount:'42',videoCount:'1'},contentDetails:{relatedPlaylists:{uploads:slug}}}]});
    if(url.pathname==='/youtube/v3/playlistItems') return response({items:[{contentDetails:{videoId:videos[slug]}}]});
    if(url.pathname==='/youtube/v3/videos') return response({items:[{id:videos[slug],snippet:{channelId:channels[slug],title:'Fixture film',publishedAt:'2026-11-01T18:00:00Z',description:''},statistics:{viewCount:'42',likeCount:'3',commentCount:'1'},contentDetails:{duration:'PT10M'},status:{privacyStatus:'public'}}]});
  }
  if(url.hostname==='youtubeanalytics.googleapis.com' && url.pathname==='/v2/reports') {
    const dimensions=(url.searchParams.get('dimensions')||'').split(',').filter(Boolean);
    const metrics=url.searchParams.get('metrics').split(',');
    const values={day:'2026-11-18',video:videos[slug],insightTrafficSourceType:'YT_SEARCH',elapsedVideoTimeRatio:0.05,country:'GB',ageGroup:'age25-34',insightTrafficSourceDetail:'fixturepeer',views:42,estimatedMinutesWatched:20,subscribersGained:2,subscribersLost:0,averageViewDuration:120,averageViewPercentage:20,audienceWatchRatio:0.7,relativeRetentionPerformance:0.5};
    const columns=[...dimensions,...metrics];
    return response({columnHeaders:columns.map(name=>({name})),rows:[columns.map(name=>values[name]??0)]});
  }
  throw new Error('Unexpected endpoint in analytics fixture');
};
