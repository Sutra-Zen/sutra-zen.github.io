// S12's three vine-bordered panels on the intact 1374 x 768 illustration.
// Full-image cells are clipped along the painted dividers in book.css.
// Select by original paragraph, so split captions keep the same active panel.
const PANEL_FOCUS = {
  coordinateBasis: 'displayed-image-percent',
  scenes: {
    S12: {
      panels: [
        {id: 's12-left', label: '左格：樂顛倒', x: 0, y: 0, width: 100, height: 100},
        {id: 's12-middle', label: '中格：觀受是苦', x: 0, y: 0, width: 100, height: 100},
        {id: 's12-right', label: '右格：離苦解脫', x: 0, y: 0, width: 100, height: 100},
      ],
      pages: ['s12-left', 's12-middle', 's12-middle', 's12-right'],
    },
  },
};
