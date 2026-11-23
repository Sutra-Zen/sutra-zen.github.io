// Genuine watercolor sprite atlas coordinates; original PNGs remain intact.
// Geometry is in source-image pixels. All labels live in HTML, not this art.
const resolveAsset = path => new URL(path, import.meta.url).href;
export const ART_VERSION = '2026-11-23-modular-city-concept-1';
export const WORLD_SIZE = Object.freeze({width:1600,height:900});
export const ART_MANIFEST = Object.freeze({
  "ground": {
    "path": "assets/ground-concept.png",
    "width": 1672,
    "height": 941,
    "mode": "RGB",
    "bytes": 3101137,
    "sha256": "097a6b5b4557d3bd50f6a9b38f15b03bd4eace6040a721de9787e8450f65c603",
    "originalOutput": "/workspace/generated_images/exec-2a6bc4d8-5366-43db-9310-46d378885bfb.png"
  },
  "gates": {
    "path": "assets/gates-atlas-concept.png",
    "width": 1536,
    "height": 1024,
    "mode": "RGBA",
    "bytes": 2380798,
    "sha256": "23de7a78f9a366d9a93178c0f67c3721b6d41de7ede93fc2fe15c0770520fab2",
    "originalOutput": "/workspace/generated_images/exec-3d57e0ad-1192-4fba-86e3-b7b99a8059df.png",
    "alphaExtrema": [
      0,
      254
    ]
  },
  "buildings": {
    "path": "assets/buildings-atlas-concept.png",
    "width": 1536,
    "height": 1024,
    "mode": "RGBA",
    "bytes": 2919911,
    "sha256": "351c775b7966aa3e9e8cf9b54803ec8bfa0416e292504ea01d3ac338d94cf376",
    "originalOutput": "/workspace/generated_images/exec-bd694bbe-7d47-446e-90f6-237f4b82131a.png",
    "alphaExtrema": [
      0,
      253
    ]
  },
  "cast": {
    "path": "assets/cast-atlas-concept.png",
    "width": 1536,
    "height": 1024,
    "mode": "RGBA",
    "bytes": 2330072,
    "sha256": "3ff47b60815232fd13cac93faf48183a8c708e32f526bd1bd773f6d9f1e38f33",
    "originalOutput": "/workspace/generated_images/exec-13cfa223-fbdf-49f7-959d-aaddf3cc7d36.png",
    "alphaExtrema": [
      0,
      254
    ]
  },
  "jhanas": {
    "path": "assets/jhanas-atlas-concept.png",
    "width": 1254,
    "height": 1254,
    "mode": "RGBA",
    "bytes": 2280641,
    "sha256": "fd925e7f47068c9c7eda7ed0098e66d6f3a1c313ec9a59f95e9a5eaf0e44c8d3",
    "originalOutput": "/workspace/generated_images/exec-aca760d4-27d6-44a6-9761-74e049502255.png",
    "alphaExtrema": [
      0,
      255
    ]
  },
  "hindrances": {
    "path": "assets/hindrances-atlas-concept.png",
    "width": 1254,
    "height": 1254,
    "mode": "RGBA",
    "bytes": 2347719,
    "sha256": "bbfc44b0c43622344a63055445e3bbbd81d264b67f3fa56b7565768744469eda",
    "originalOutput": "/workspace/generated_images/exec-03ae593e-b56e-47cb-b0f9-53cd7bf7c5fb.png",
    "alphaExtrema": [
      0,
      255
    ]
  },
  "companions": {
    "path": "assets/companions-atlas-concept.png",
    "width": 1536,
    "height": 1024,
    "mode": "RGBA",
    "bytes": 1869168,
    "sha256": "0df16b53b52788dcd2fbf4624bce389ff6e884a6cc47ebfc921d3eb6dbc61440",
    "originalOutput": "/workspace/generated_images/exec-b47d6010-7d8b-4300-ae35-2933c82a1cd1.png",
    "alphaExtrema": [
      0,
      254
    ]
  },
  "dock": {
    "path": "../../visual-v2/assets/city-dharma-dock-concept.png",
    "width": 1536,
    "height": 1024,
    "mode": "RGBA",
    "bytes": 2069123,
    "sha256": "2bbe41bd04e24a9ca5c78bbdc00a0318f19c052d8ff5d9c2548e569b4545bd22",
    "alphaExtrema": [
      0,
      254
    ]
  },
  "mara": {
    "path": "assets/mara-fullbody-concept.png",
    "width": 1024,
    "height": 1536,
    "mode": "RGBA",
    "bytes": 2426710,
    "sha256": "ec09957c3962f01382ebc9cc99264ea35b092c476c8d57781843e4e6f4765ba4",
    "originalOutput": "/workspace/generated_images/exec-76d53aa2-4ebd-4c5a-9975-252dcd6edf60.png",
    "alphaExtrema": [
      0,
      254
    ]
  },
  "doubt": {
    "path": "../../story/assets/doubt-creature-concept.png",
    "width": 1254,
    "height": 1254,
    "mode": "RGBA",
    "bytes": 2066489,
    "sha256": "49f418241e4969e5c7d1da625620bd4aa5a2d1c0177b94f5c1be0c8e26dbc361",
    "alphaExtrema": [
      0,
      255
    ]
  },
  "lord_hair": {
    "path": "../../visual-v2/assets/city-lord-facial-hair-layer.png",
    "width": 1536,
    "height": 1024,
    "mode": "RGBA",
    "bytes": 2154990,
    "sha256": "8a1bc7638be862d85090b678a4be4a30855bfd70392b36ccb417ae0beaf1a300",
    "alphaExtrema": [
      0,
      254
    ]
  }
});
const spriteRecords = {
  "gate_n": {
    "asset": "gates",
    "x": 53,
    "y": 74,
    "w": 444,
    "h": 366,
    "width": 444,
    "height": 366,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      0,
      512,
      512
    ],
    "alpha32Bounds": [
      61,
      82,
      489,
      432
    ]
  },
  "gate_ne": {
    "asset": "gates",
    "x": 557,
    "y": 65,
    "w": 408,
    "h": 385,
    "width": 408,
    "height": 385,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      512,
      0,
      512,
      512
    ],
    "alpha32Bounds": [
      565,
      73,
      957,
      442
    ]
  },
  "gate_se": {
    "asset": "gates",
    "x": 1081,
    "y": 65,
    "w": 410,
    "h": 385,
    "width": 410,
    "height": 385,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      1024,
      0,
      512,
      512
    ],
    "alpha32Bounds": [
      1089,
      73,
      1483,
      442
    ]
  },
  "gate_s": {
    "asset": "gates",
    "x": 48,
    "y": 571,
    "w": 450,
    "h": 373,
    "width": 450,
    "height": 373,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      512,
      512,
      512
    ],
    "alpha32Bounds": [
      56,
      579,
      490,
      936
    ]
  },
  "gate_sw": {
    "asset": "gates",
    "x": 563,
    "y": 543,
    "w": 403,
    "h": 407,
    "width": 403,
    "height": 407,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      512,
      512,
      512,
      512
    ],
    "alpha32Bounds": [
      571,
      551,
      958,
      942
    ]
  },
  "gate_nw": {
    "asset": "gates",
    "x": 1080,
    "y": 543,
    "w": 404,
    "h": 407,
    "width": 404,
    "height": 407,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      1024,
      512,
      512,
      512
    ],
    "alpha32Bounds": [
      1088,
      551,
      1476,
      942
    ]
  },
  "base_garden": {
    "asset": "buildings",
    "x": 20,
    "y": 19,
    "w": 350,
    "h": 306,
    "width": 350,
    "height": 306,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      0,
      384,
      341
    ],
    "alpha32Bounds": [
      28,
      27,
      362,
      317
    ]
  },
  "city_outline": {
    "asset": "buildings",
    "x": 398,
    "y": 40,
    "w": 355,
    "h": 268,
    "width": 355,
    "height": 268,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      384,
      0,
      384,
      341
    ],
    "alpha32Bounds": [
      406,
      48,
      745,
      300
    ]
  },
  "aggregates_corner": {
    "asset": "buildings",
    "x": 783,
    "y": 29,
    "w": 351,
    "h": 288,
    "width": 351,
    "height": 288,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      768,
      0,
      384,
      341
    ],
    "alpha32Bounds": [
      791,
      37,
      1126,
      309
    ]
  },
  "conditions_wheel": {
    "asset": "buildings",
    "x": 1174,
    "y": 23,
    "w": 339,
    "h": 300,
    "width": 339,
    "height": 300,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      1152,
      0,
      384,
      341
    ],
    "alpha32Bounds": [
      1182,
      31,
      1505,
      315
    ]
  },
  "noble_path": {
    "asset": "buildings",
    "x": 34,
    "y": 369,
    "w": 304,
    "h": 285,
    "width": 304,
    "height": 285,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      341,
      384,
      342
    ],
    "alpha32Bounds": [
      42,
      377,
      330,
      646
    ]
  },
  "confidence_harbor": {
    "asset": "buildings",
    "x": 402,
    "y": 351,
    "w": 352,
    "h": 301,
    "width": 352,
    "height": 301,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      384,
      341,
      384,
      342
    ],
    "alpha32Bounds": [
      410,
      359,
      746,
      644
    ]
  },
  "guard_post": {
    "asset": "buildings",
    "x": 795,
    "y": 364,
    "w": 319,
    "h": 288,
    "width": 319,
    "height": 288,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      768,
      341,
      384,
      342
    ],
    "alpha32Bounds": [
      803,
      372,
      1106,
      644
    ]
  },
  "effort_garden": {
    "asset": "buildings",
    "x": 1160,
    "y": 368,
    "w": 365,
    "h": 271,
    "width": 365,
    "height": 271,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      1152,
      341,
      384,
      342
    ],
    "alpha32Bounds": [
      1168,
      376,
      1517,
      631
    ]
  },
  "bamboo": {
    "asset": "buildings",
    "x": 17,
    "y": 686,
    "w": 344,
    "h": 313,
    "width": 344,
    "height": 313,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      683,
      384,
      341
    ],
    "alpha32Bounds": [
      25,
      694,
      353,
      991
    ]
  },
  "endeavor_boat": {
    "asset": "buildings",
    "x": 403,
    "y": 687,
    "w": 345,
    "h": 313,
    "width": 345,
    "height": 313,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      384,
      683,
      384,
      341
    ],
    "alpha32Bounds": [
      411,
      695,
      740,
      992
    ]
  },
  "faculties_links": {
    "asset": "buildings",
    "x": 790,
    "y": 691,
    "w": 332,
    "h": 301,
    "width": 332,
    "height": 301,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      768,
      683,
      384,
      341
    ],
    "alpha32Bounds": [
      798,
      699,
      1114,
      984
    ]
  },
  "fruition_guide": {
    "asset": "buildings",
    "x": 1162,
    "y": 714,
    "w": 363,
    "h": 269,
    "width": 363,
    "height": 269,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      1152,
      683,
      384,
      341
    ],
    "alpha32Bounds": [
      1170,
      722,
      1517,
      975
    ]
  },
  "city_lord": {
    "asset": "cast",
    "x": 56,
    "y": 7,
    "w": 384,
    "h": 475,
    "width": 384,
    "height": 475,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      0,
      512,
      512
    ],
    "alpha32Bounds": [
      64,
      15,
      432,
      474
    ],
    "attachments": [
      {
        "assetKey": "lord_facial_hair",
        "xPct": 22.4,
        "yPct": 39,
        "widthPct": 70.3,
        "heightPct": 36.8
      }
    ]
  },
  "mindfulness_guard": {
    "asset": "cast",
    "x": 580,
    "y": 76,
    "w": 336,
    "h": 394,
    "width": 336,
    "height": 394,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      512,
      0,
      512,
      512
    ],
    "alpha32Bounds": [
      588,
      84,
      908,
      462
    ]
  },
  "calm_messenger": {
    "asset": "cast",
    "x": 1105,
    "y": 35,
    "w": 356,
    "h": 440,
    "width": 356,
    "height": 440,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      1024,
      0,
      512,
      512
    ],
    "alpha32Bounds": [
      1113,
      43,
      1453,
      467
    ]
  },
  "insight_messenger": {
    "asset": "cast",
    "x": 80,
    "y": 555,
    "w": 344,
    "h": 428,
    "width": 344,
    "height": 428,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      512,
      512,
      512
    ],
    "alpha32Bounds": [
      88,
      563,
      416,
      975
    ]
  },
  "scroll": {
    "asset": "cast",
    "x": 525,
    "y": 619,
    "w": 444,
    "h": 305,
    "width": 444,
    "height": 305,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      512,
      512,
      512,
      512
    ],
    "alpha32Bounds": [
      533,
      627,
      961,
      916
    ]
  },
  "messenger_pair": {
    "asset": "cast",
    "x": 1058,
    "y": 558,
    "w": 449,
    "h": 417,
    "width": 449,
    "height": 417,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      1024,
      512,
      512,
      512
    ],
    "alpha32Bounds": [
      1066,
      566,
      1499,
      967
    ]
  },
  "lord_facial_hair": {
    "asset": "lord_hair",
    "x": 42,
    "y": 77,
    "w": 1452,
    "h": 903,
    "width": 1452,
    "height": 903,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      0,
      1536,
      1024
    ],
    "alpha32Bounds": [
      50,
      85,
      1486,
      972
    ]
  },
  "messengers": {
    "asset": "cast",
    "x": 1058,
    "y": 558,
    "w": 449,
    "h": 417,
    "width": 449,
    "height": 417,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      1024,
      512,
      512,
      512
    ],
    "alpha32Bounds": [
      1066,
      566,
      1499,
      967
    ],
    "attachments": [
      {
        "assetKey": "scroll",
        "xPct": 10,
        "yPct": 42,
        "widthPct": 80,
        "heightPct": 26
      }
    ]
  },
  "jhana_bath": {
    "asset": "jhanas",
    "x": 53,
    "y": 53,
    "w": 538,
    "h": 535,
    "width": 538,
    "height": 535,
    "atlasWidth": 1254,
    "atlasHeight": 1254,
    "cellRect": [
      0,
      0,
      627,
      627
    ],
    "alpha32Bounds": [
      61,
      61,
      583,
      580
    ]
  },
  "jhana_spring": {
    "asset": "jhanas",
    "x": 627,
    "y": 55,
    "w": 589,
    "h": 544,
    "width": 589,
    "height": 544,
    "atlasWidth": 1254,
    "atlasHeight": 1254,
    "cellRect": [
      627,
      0,
      627,
      627
    ],
    "alpha32Bounds": [
      633,
      63,
      1208,
      591
    ]
  },
  "jhana_lotus": {
    "asset": "jhanas",
    "x": 22,
    "y": 653,
    "w": 589,
    "h": 545,
    "width": 589,
    "height": 545,
    "atlasWidth": 1254,
    "atlasHeight": 1254,
    "cellRect": [
      0,
      627,
      627,
      627
    ],
    "alpha32Bounds": [
      30,
      661,
      603,
      1190
    ]
  },
  "jhana_cloth": {
    "asset": "jhanas",
    "x": 644,
    "y": 694,
    "w": 581,
    "h": 476,
    "width": 581,
    "height": 476,
    "atlasWidth": 1254,
    "atlasHeight": 1254,
    "cellRect": [
      627,
      627,
      627,
      627
    ],
    "alpha32Bounds": [
      652,
      702,
      1217,
      1162
    ]
  },
  "jhana_garden": {
    "asset": "jhanas",
    "x": 22,
    "y": 53,
    "w": 1203,
    "h": 1145,
    "width": 1203,
    "height": 1145,
    "atlasWidth": 1254,
    "atlasHeight": 1254,
    "cellRect": [
      0,
      0,
      1254,
      1254
    ],
    "alpha32Bounds": [
      30,
      61,
      1217,
      1190
    ]
  },
  "companion_owl": {
    "asset": "companions",
    "x": 104,
    "y": 109,
    "w": 335,
    "h": 297,
    "width": 335,
    "height": 297,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      0,
      512,
      512
    ],
    "alpha32Bounds": [
      112,
      117,
      431,
      398
    ]
  },
  "companion_rabbit": {
    "asset": "companions",
    "x": 616,
    "y": 102,
    "w": 324,
    "h": 304,
    "width": 324,
    "height": 304,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      512,
      0,
      512,
      512
    ],
    "alpha32Bounds": [
      624,
      110,
      932,
      398
    ]
  },
  "companion_bird": {
    "asset": "companions",
    "x": 1103,
    "y": 132,
    "w": 324,
    "h": 243,
    "width": 324,
    "height": 243,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      1024,
      0,
      512,
      512
    ],
    "alpha32Bounds": [
      1111,
      140,
      1419,
      367
    ]
  },
  "companion_turtle": {
    "asset": "companions",
    "x": 133,
    "y": 650,
    "w": 301,
    "h": 236,
    "width": 301,
    "height": 236,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      512,
      512,
      512
    ],
    "alpha32Bounds": [
      141,
      658,
      426,
      878
    ]
  },
  "companion_lotus": {
    "asset": "companions",
    "x": 600,
    "y": 642,
    "w": 331,
    "h": 257,
    "width": 331,
    "height": 257,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      512,
      512,
      512,
      512
    ],
    "alpha32Bounds": [
      608,
      650,
      923,
      891
    ]
  },
  "companion_deer": {
    "asset": "companions",
    "x": 1121,
    "y": 611,
    "w": 302,
    "h": 302,
    "width": 302,
    "height": 302,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      1024,
      512,
      512,
      512
    ],
    "alpha32Bounds": [
      1129,
      619,
      1415,
      905
    ]
  },
  "awakening_companions": {
    "asset": "companions",
    "x": 104,
    "y": 102,
    "w": 1323,
    "h": 811,
    "width": 1323,
    "height": 811,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      0,
      1536,
      1024
    ],
    "alpha32Bounds": [
      112,
      110,
      1419,
      905
    ]
  },
  "hindrance_desire": {
    "asset": "hindrances",
    "x": 34,
    "y": 44,
    "w": 579,
    "h": 548,
    "width": 579,
    "height": 548,
    "atlasWidth": 1254,
    "atlasHeight": 1254,
    "cellRect": [
      0,
      0,
      627,
      627
    ],
    "alpha32Bounds": [
      42,
      52,
      605,
      584
    ]
  },
  "hindrance_anger": {
    "asset": "hindrances",
    "x": 656,
    "y": 16,
    "w": 569,
    "h": 572,
    "width": 569,
    "height": 572,
    "atlasWidth": 1254,
    "atlasHeight": 1254,
    "cellRect": [
      627,
      0,
      627,
      627
    ],
    "alpha32Bounds": [
      664,
      24,
      1217,
      580
    ]
  },
  "hindrance_sloth": {
    "asset": "hindrances",
    "x": 54,
    "y": 673,
    "w": 540,
    "h": 529,
    "width": 540,
    "height": 529,
    "atlasWidth": 1254,
    "atlasHeight": 1254,
    "cellRect": [
      0,
      627,
      627,
      627
    ],
    "alpha32Bounds": [
      62,
      681,
      586,
      1194
    ]
  },
  "hindrance_restlessness": {
    "asset": "hindrances",
    "x": 631,
    "y": 640,
    "w": 592,
    "h": 579,
    "width": 592,
    "height": 579,
    "atlasWidth": 1254,
    "atlasHeight": 1254,
    "cellRect": [
      627,
      627,
      627,
      627
    ],
    "alpha32Bounds": [
      639,
      648,
      1215,
      1211
    ]
  },
  "truth_dock": {
    "asset": "dock",
    "x": 115,
    "y": 27,
    "w": 1286,
    "h": 956,
    "width": 1286,
    "height": 956,
    "atlasWidth": 1536,
    "atlasHeight": 1024,
    "cellRect": [
      0,
      0,
      1536,
      1024
    ],
    "alpha32Bounds": [
      123,
      35,
      1393,
      975
    ]
  },
  "mara": {
    "asset": "mara",
    "x": 45,
    "y": 144,
    "w": 931,
    "h": 1193,
    "width": 931,
    "height": 1193,
    "atlasWidth": 1024,
    "atlasHeight": 1536,
    "cellRect": [
      0,
      0,
      1024,
      1536
    ],
    "alpha32Bounds": [
      53,
      152,
      968,
      1329
    ]
  },
  "hindrance_doubt": {
    "asset": "doubt",
    "x": 80,
    "y": 114,
    "w": 1094,
    "h": 1022,
    "width": 1094,
    "height": 1022,
    "atlasWidth": 1254,
    "atlasHeight": 1254,
    "cellRect": [
      0,
      0,
      1254,
      1254
    ],
    "alpha32Bounds": [
      88,
      122,
      1166,
      1128
    ]
  }
};
for (const art of Object.values(spriteRecords)) {
  const asset = ART_MANIFEST[art.asset];
  art.url = resolveAsset(asset.path); art.src = art.url;
  art.status = 'generated-concept'; art.sourceSHA256 = asset.sha256;
  Object.freeze(art);
}
const aliases = {
  "lord": "city_lord",
  "guardian": "mindfulness_guard",
  "hindrance_ill_will": "hindrance_anger",
  "companion_bluebird": "companion_bird",
  "faculty_glow": "faculties_links",
  "mindfulness_glow": "mindfulness_guard"
};
for (const [alias, original] of Object.entries(aliases)) spriteRecords[alias] = spriteRecords[original];
export const sprites = Object.freeze(spriteRecords);
export const ground = Object.freeze({...ART_MANIFEST.ground,
  url:resolveAsset(ART_MANIFEST.ground.path),src:resolveAsset(ART_MANIFEST.ground.path),status:'generated-concept'});
// Both nested and flat access are supported for the scene and dialogue heads.
export const CITY_MODULE_ART = Object.freeze({ground,sprites,...sprites});
