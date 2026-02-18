// Central export for all game templates
// Each genre has its own file with complete, playable game code

import { TYCOON_TEMPLATE } from './tycoon';
import { OBBY_TEMPLATE } from './obby';
import { SIMULATOR_TEMPLATE } from './simulator';
import { RPG_TEMPLATE } from './rpg';
import { HORROR_TEMPLATE } from './horror';

export const GAME_TEMPLATES = {
  tycoon: TYCOON_TEMPLATE,
  obby: OBBY_TEMPLATE,
  simulator: SIMULATOR_TEMPLATE,
  rpg: RPG_TEMPLATE,
  horror: HORROR_TEMPLATE,
};

export { TYCOON_TEMPLATE, OBBY_TEMPLATE, SIMULATOR_TEMPLATE, RPG_TEMPLATE, HORROR_TEMPLATE };
