import { STORY_UI } from './data.js?v=character-pronouns-1';

// Presentation only. Reading eligibility, completion and saved story flags are
// owned by the caller; this stage never writes storage or advances the story.
const STATES = new Set(['hidden', 'waiting', 'thinning', 'receding']);
const MARKS = Object.freeze([
  [10, 20, -18, 1.1], [32, 3, -10, .95], [70, 0, 12, 1.1],
  [97, 23, 18, .9], [6, 65, -14, .85], [98, 72, 14, .9], [55, -10, -5, .85],
]);

export function initializeDoubtStage({ world, anchor = { x: 1248, y: 566 } } = {}) {
  if (!world?.append) return { update() {}, destroy() {} };
  const element = document.createElement('div');
  element.className = 'doubt-stage'; element.dataset.doubtStage = '';
  element.dataset.doubtState = 'hidden'; element.hidden = true;
  element.setAttribute('role', 'img');
  element.setAttribute('aria-label', STORY_UI.doubtStageLabel);
  element.style.left = (Number.isFinite(anchor.x) ? anchor.x : 1248) + 'px';
  element.style.top = (Number.isFinite(anchor.y) ? anchor.y : 566) + 'px';

  const mist = document.createElement('span');
  mist.className = 'doubt-stage__mist'; mist.setAttribute('aria-hidden', 'true');
  const creature = document.createElement('img');
  creature.className = 'doubt-stage__creature'; creature.alt = '';
  creature.width = 1254; creature.height = 1254; creature.draggable = false;
  creature.src = new URL('./assets/doubt-creature-concept.png', import.meta.url).href;
  let artFailed = false;
  creature.addEventListener('error', () => { artFailed = true; element.hidden = true; });
  element.append(mist, creature);
  MARKS.forEach(([x, y, angle, scale], index) => {
    const mark = document.createElement('span');
    mark.className = 'story-doubt-mark'; mark.dataset.doubtMark = String(index + 1);
    mark.setAttribute('aria-hidden', 'true'); mark.textContent = STORY_UI.questionMark;
    mark.style.setProperty('--mark-x', x + '%'); mark.style.setProperty('--mark-y', y + '%');
    mark.style.setProperty('--mark-angle', angle + 'deg'); mark.style.setProperty('--mark-size', String(scale));
    element.append(mark);
  });
  world.append(element);
  let state = 'hidden', destroyed = false;
  return {
    update({ state: next } = {}) {
      if (destroyed || !STATES.has(next) || next === state) return;
      state = next; element.dataset.doubtState = next; element.hidden = next === 'hidden' || artFailed;
      element.setAttribute('aria-hidden', String(next === 'hidden' || next === 'receding'));
    },
    destroy() { if (destroyed) return; destroyed = true; element.remove(); },
  };
}
