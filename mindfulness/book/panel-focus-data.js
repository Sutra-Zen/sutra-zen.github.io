// Presentation-only focus after visually checking all 25 original scenes.
// Select by original paragraph unless an existing split caption explicitly
// describes a smaller panel group (by: 'page'). No narration is repaginated.
// Full-image cells follow original dividers through local book.css polygons.
const PANEL_FOCUS = {
  coordinateBasis: 'displayed-image-percent',
  scenes: {
    S11: {
      by: 'page',
      panels: [
        {id: 's11-first-four', label: '前四格：飽滿、發脹、腐壞、啃食', x: 0, y: 0, width: 100, height: 100},
        {id: 's11-last-two', label: '後兩格：果核與灰土', x: 0, y: 0, width: 100, height: 100},
      ],
      pages: ['s11-first-four', 's11-last-two', null, null, null],
    },
    S12: {
      panels: [
        {id: 's12-left', label: '左格：樂顛倒', x: 0, y: 0, width: 100, height: 100},
        {id: 's12-middle', label: '中格：觀受是苦', x: 0, y: 0, width: 100, height: 100},
        {id: 's12-right', label: '右格：離苦解脫', x: 0, y: 0, width: 100, height: 100},
      ],
      pages: ['s12-left', 's12-middle', 's12-middle', 's12-right'],
    },
    S13: {
      panels: [
        {id: 's13-left', label: '左格：樂受生起', x: 0, y: 0, width: 50, height: 100},
        {id: 's13-right', label: '右格：便知樂受生起', x: 50, y: 0, width: 50, height: 100},
      ],
      pages: [null, 's13-left', 's13-left', 's13-right', 's13-right'],
    },
    S14: {
      panels: [
        {id: 's14-left', label: '左格：苦受生起', x: 0, y: 0, width: 50, height: 100},
        {id: 's14-right', label: '右格：便知苦受生起', x: 50, y: 0, width: 50, height: 100},
      ],
      pages: [null, 's14-left', 's14-left', 's14-right', 's14-right'],
    },
    S15: {
      panels: [
        {id: 's15-body-mind', label: '第一欄上下對照：身與心', x: 0, y: 0, width: 100, height: 100},
        {id: 's15-food-without-food', label: '第二欄上下對照：食與無食', x: 0, y: 0, width: 100, height: 100},
        {id: 's15-desire-without-desire', label: '第三欄上下對照：欲與無欲', x: 0, y: 0, width: 100, height: 100},
      ],
      pages: [null, 's15-body-mind', 's15-food-without-food', 's15-desire-without-desire', null],
    },
    S21: {
      by: 'page',
      panels: [
        {id: 's21-left', label: '左格：怒氣升起', x: 0, y: 0, width: 50, height: 100},
        {id: 's21-right', label: '右格：怒氣消融', x: 50, y: 0, width: 50, height: 100},
      ],
      pages: [null, null, 's21-right', null],
    },
  },
};
