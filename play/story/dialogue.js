import { STORY_ACTORS, STORY_SCENES, STORY_UI as T } from './data.js';
import { storyStore } from './store.js?v=prologue-1';

export function initializeStoryDialogue({ host, onAction, onClose } = {}) {
  if (!host) throw Error('Missing story dialogue host.');
  const panel = document.createElement('section');
  panel.className = 'story-dialogue'; panel.hidden = true;
  panel.setAttribute('aria-label', T.dialogue);
  panel.innerHTML = '<div class="story-dialogue__portrait"><img alt="" width="1254" height="1254"></div>' +
    '<div class="story-dialogue__body"><h2 id="story-speaker"></h2><p id="story-line" class="story-dialogue__line"></p>' +
    '<p class="story-dialogue__notice" role="status" hidden></p></div>' +
    '<div class="story-dialogue__actions"><button class="story-dialogue__skip"></button><button class="story-dialogue__next" aria-describedby="story-line"></button></div>';
  host.append(panel);
  let current = null, replay = false, previousFocus = null;
  const image = panel.querySelector('img');
  image.addEventListener('error', () => { image.hidden = true; panel.classList.add('story-dialogue--no-art'); });
  image.addEventListener('load', () => { image.hidden = false; panel.classList.remove('story-dialogue--no-art'); });
  function close({ restoreFocus = true } = {}) {
    panel.hidden = true; current = null;
    host.classList.remove('has-story-dialogue');
    if (restoreFocus) {
      if (previousFocus?.isConnected && previousFocus.getClientRects().length) previousFocus.focus({ preventScroll: true });
      else onClose?.();
    }
  }
  panel.querySelector('.story-dialogue__skip').addEventListener('click', () => close());
  panel.querySelector('.story-dialogue__next').addEventListener('click', () => {
    if (!current) return;
    const scene = current, reviewing = replay;
    close({ restoreFocus: false });
    onAction?.(scene, { replay: reviewing });
  });
  panel.addEventListener('keydown', event => { if (event.key === 'Escape') { event.preventDefault(); close(); } });
  return {
    show(id, { replay: reviewing = false, focus = true } = {}) {
      const scene = STORY_SCENES[id], actor = scene && STORY_ACTORS[scene.actorId];
      if (!actor) return false;
      previousFocus = document.activeElement; current = scene; replay = reviewing;
      panel.dataset.scene = id; panel.dataset.actor = scene.actorId;
      panel.querySelector('h2').textContent = actor.name;
      panel.querySelector('.story-dialogue__line').textContent = scene.text;
      panel.querySelector('.story-dialogue__skip').textContent = T.skip;
      panel.querySelector('.story-dialogue__next').textContent = replay ? T.returnToMap : T.enter;
      image.hidden = false; image.src = actor.portrait;
      if (!reviewing) storyStore.markSeen(id);
      const notice = panel.querySelector('.story-dialogue__notice');
      notice.textContent = storyStore.issue === 'corrupt' ? T.storageCorrupt : storyStore.issue ? T.storageUnavailable : '';
      notice.hidden = !notice.textContent;
      panel.hidden = false; host.classList.add('has-story-dialogue');
      if (focus) panel.querySelector('.story-dialogue__next').focus({ preventScroll: true });
      return true;
    },
    close,
    get isOpen() { return !panel.hidden; },
  };
}
