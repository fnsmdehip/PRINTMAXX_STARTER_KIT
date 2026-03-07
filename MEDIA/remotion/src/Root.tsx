import React from 'react';
import {Composition} from 'remotion';
import {SocialHook} from './compositions/SocialHook';
import {StatsDashboard} from './compositions/StatsDashboard';
import {QuoteCard} from './compositions/QuoteCard';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="SocialHook"
        component={SocialHook}
        durationInFrames={150}
        fps={30}
        width={1200}
        height={675}
        defaultProps={{
          hookText: 'i monitor 200+ competitor pages. they update something, i know in 30 seconds.',
          highlightWord: '200+ competitor pages',
          subtitle: 'the system that runs while you sleep',
        }}
      />
      <Composition
        id="StatsDashboard"
        component={StatsDashboard}
        durationInFrames={150}
        fps={30}
        width={1200}
        height={675}
        defaultProps={{
          title: 'system status — last 24 hours',
          subtitle: 'autonomous agent performance dashboard',
          stats: [
            {value: '24', label: 'Active Agents', delta: '+2 today'},
            {value: '142', label: 'Tasks Run', delta: '+38 vs yesterday'},
            {value: '89%', label: 'Success Rate', delta: '+12% this week'},
            {value: '$0', label: 'Revenue', delta: 'soon'},
          ],
        }}
      />
      <Composition
        id="QuoteCard"
        component={QuoteCard}
        durationInFrames={120}
        fps={30}
        width={1080}
        height={1080}
        defaultProps={{
          quote: 'stop overthinking this. just set up the alerts and start watching.',
          attribution: 'PRINTMAXX',
        }}
      />
    </>
  );
};
