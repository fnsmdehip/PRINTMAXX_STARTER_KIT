import React from 'react';
import {Composition} from 'remotion';
import {SocialHook} from './compositions/SocialHook';
import {StatsDashboard} from './compositions/StatsDashboard';
import {QuoteCard} from './compositions/QuoteCard';
import {PipelinePressure} from './compositions/PipelinePressure';

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
      <Composition
        id="PipelinePressure"
        component={PipelinePressure}
        durationInFrames={180}
        fps={30}
        width={1200}
        height={675}
        defaultProps={{
          headline: 'pipeline status — day 32 at $0 revenue',
          stats: [
            {value: '131', label: 'Products Built', color: '#667eea'},
            {value: '32', label: 'Agents Running', color: '#764ba2'},
            {value: '$3.4K', label: 'Monthly Pipeline', color: '#f093fb'},
            {value: '0', label: 'Listed', color: '#f5576c'},
          ],
          punchline: 'the swarm is a loaded gun. someone needs to pull the trigger.',
        }}
      />
    </>
  );
};
