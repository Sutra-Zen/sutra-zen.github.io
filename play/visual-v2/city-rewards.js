// Runtime presentation of the existing r3 rewards. This module has no store,
// completion writes, or invented canonical correspondences. Source art is shown
// through SVG viewports; these are not new transparent production character art.
const asset=path=>new URL(path,import.meta.url).href;
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const CITY_REWARD_SOURCES=Object.freeze({
 companions:{path:'../../seven-factors/assets/12.webp',width:1672,height:941},
 jhanas:{path:'../../four-jhanas/assets/S10.webp',width:1672,height:941},
 wheel:{path:'../../twelve-links/assets/wheel-of-life.jpg',width:5460,height:7170},
 wholesome:{path:'../../docs/eightfold-path/assets/05-wholesome-actions.webp',width:2752,height:1536},
 effort:{path:'../../docs/right-effort/assets/ABB524ED-47E1-4E5F-9F67-C308209E0B8B.png',width:1672,height:941},
 fruition:{path:'../../docs/four-fruits-ten-fetters/assets/s06.webp',width:1376,height:768},
 boat:{path:'assets/kitten-rowboat-concept.png'},garden:{path:'assets/garden-growth-concept.png'},
});
export const AWAKENING_COMPANIONS=Object.freeze([
 {id:'mindfulness',title:'念',role:'念-守門人',existingGuardian:true,x:29,y:63},
 {id:'investigation',title:'擇法',role:'貓頭鷹',crop:[300,65,340,240],x:9,y:18,w:9},
 {id:'effort',title:'精進',role:'兔子',crop:[165,300,330,285],x:95,y:69,w:9},
 {id:'joy',title:'喜',role:'藍鳥',crop:[705,10,260,235],x:35,y:23,w:8},
 {id:'tranquility',title:'輕安',role:'烏龜',crop:[1090,95,285,250],x:91,y:51,w:9},
 {id:'concentration',title:'定',role:'蓮花',crop:[1205,320,315,245],x:33,y:49,w:9},
 {id:'equanimity',title:'捨',role:'小鹿',crop:[1110,520,285,320],x:31,y:89,w:8},
]);
// Locations refer to the existing dock, flower garden, guardian, quiet garden,
// and Dharma-wheel dock; no second guardian or new concentration building.
export const FACULTY_ZONES=Object.freeze({
 faith:{x:15,y:82,title:'信・信心港灣'},effort:{x:65,y:73,title:'精進・照料花園'},
 mindfulness:{x:29,y:63,title:'念・念-守門人'},concentration:{x:36,y:22,title:'定・靜水庭園'},
 wisdom:{x:18,y:83,title:'慧・四聖諦法輪'},
});
export const CITY_REWARD_COPY=Object.freeze({
 truth_dock:'法輪碼頭是四聖諦故事的遊戲延伸。法輪留在碼頭，中央廣場仍對應四大。',
 city_body:'城體、四大廣場與識城主沿用SN35.245原喻；城中日常事件的觀察安排是繪本延伸。',
 six_gates:'眼、耳、鼻、舌、身、意六內處對應六門。城門景物與顯現時機是遊戲美術。',
 conditions_wheel:'城側的緣起輪庭回看十二因緣。它是繪本延伸，不取代城中對應四大的廣場。',
 noble_path:'往返道路譬喻八正道，屬城喻原有對應；道支提示與十善生活片段是繪本延伸。',
 confidence_harbor:'信心港灣的六盞燈對應六念的閱讀回顧，屬繪本場景延伸。',
 mindfulness_guard:'念-守門人仍是同一位持燈角色。守門人對應念屬原喻；四種觀察及四顛倒辨識屬教材延伸。',
 effort_garden:'花園以預防、拔草、播種及持續照料回看四正勤，這是依既有繪本安排的場景延伸。',
 calm_insight_messengers:'止、觀雙使是SN35.245原喻的對應；呼吸竹林與水波是安那般那繪本的場景延伸。',
 endeavor_boat:'調心小舟回看欲、勤、心、觀及鬆緊調整，屬四如意足繪本的場景延伸。',
 jhana_garden:'澡粉團、湧泉池、蓮花池及白布覆身沿用四禪繪本的既有譬喻。本場景表示讀本完成。',
 faculties_links:'依《雜阿含經》646，信、精進、念、定、慧分別呼應四不壞淨、四正勤、四念處、四禪與四聖諦。慧另回看緣起輪，屬教材延伸，不改寫慧根的經文定義。各區只隨實際已讀來源書連動。',
 awakening_companions:'同一位念-守門人提起念燈，與貓頭鷹、兔子、藍鳥、烏龜、蓮花、小鹿六位既有夥伴一起回看七覺支。念燈強化既有守門人的角色，不新增另一位念守門人。夥伴及協調城景的演出是繪本延伸。',
 fruition_guide:'果位與十結導覽沿用既有繪本的繫縛意象。這是閱讀後開放的導覽，不代表玩家獲得果位。',
});
export const REWARD_TYPE_LABELS={canonical:'SN35.245 城喻',mixed:'城喻原有對應＋繪本延伸',extended:'繪本場景延伸'};
export function sourceViewport(key,crop,{label='',className=''}={}){
 const a=CITY_REWARD_SOURCES[key],c=crop||[0,0,a.width,a.height];
 return `<svg class="city-source-viewport ${className}" viewBox="${c.join(' ')}" data-source-art="${a.path}" data-source-crop="${c.join(',')}" role="img" aria-label="${escape(label)}"><image href="${asset(a.path)}" x="0" y="0" width="${a.width}" height="${a.height}"/></svg>`;
}
function vignette(key,crop,x,y,w,label,extra=''){
 return `<span class="city-reward-vignette ${extra}" style="--x:${x}%;--y:${y}%;--w:${w}%;--ratio:${crop[2]}/${crop[3]}" aria-label="${escape(label)}">${sourceViewport(key,crop,{label})}</span>`;
}
function zoneLinks(s){
 if(!s.features.faculties_links)return '';
 const links=Object.entries(FACULTY_ZONES).filter(([id])=>s.facultiesZones[id]?.available);
 return `<div class="city-faculties-network" data-city-reward="faculties_links" data-source-category="extended"><svg class="city-faculties-paths" viewBox="0 0 1000 563" aria-hidden="true">${links.map(([id,z])=>`<path data-faculty-link="${id}" d="M${z.x*10} ${z.y*5.63}Q${50*10} ${76*5.63} ${65*10} ${73*5.63}"/>`).join('')}${s.facultiesZones.wisdom?.conditionsLinked?'<path data-faculty-conditions-link d="M180 467Q40 380 85 220"/>':''}</svg>${links.map(([id,z])=>`<span class="city-faculty-zone" data-faculty-zone="${id}" style="--x:${z.x}%;--y:${z.y}%" aria-label="${z.title}已連動"></span>`).join('')}</div>`;
}
function companions(s){
 if(!s.features.awakening_companions)return '';
 return `<div class="city-awakening-companions" data-city-reward="awakening_companions" data-source-category="extended" aria-label="念燈與六位既有夥伴">${AWAKENING_COMPANIONS.map(c=>c.existingGuardian?`<span class="city-companion city-companion--existing-guardian ${s.features.mindfulness_guard?'':'is-pending'}" data-companion="${c.id}" data-uses-existing-guardian="true" data-companion-placed="${Boolean(s.features.mindfulness_guard)}" style="--x:${c.x}%;--y:${c.y}%" aria-label="念：同一位念-守門人，念燈亮起"></span>`:`<span class="city-companion" data-companion="${c.id}">${vignette('companions',c.crop,c.x,c.y,c.w,`${c.title}・${c.role}，七覺支原圖局部`,'city-companion-art')}</span>`).join('')}</div>`;
}
export function renderCityRewards(s){
 const f=s.features,parts=[];
 if(f.conditions_wheel)parts.push(`<div data-city-reward="conditions_wheel" data-source-category="extended">${vignette('wheel',[500,1700,4450,4600],8.5,42,10,'十二因緣既有生命之輪局部','city-wheel-vignette')}</div>`);
 if(f.noble_path)parts.push(`<div data-city-reward="noble_path" data-source-category="mixed"><div class="city-path-stones" aria-label="八支提示">${['正見','正志','正語','正業','正命','正方便','正念','正定'].map((name,i)=>`<i title="${name}" style="--x:${46+(i%2)*8}%;--y:${90-i*3.8}%" aria-label="${name}"></i>`).join('')}</div>${vignette('wholesome',[1400,0,1352,750],74,74,11,'十善生活：既有繪本幫忙拾柴片段')}</div>`);
 if(f.confidence_harbor)parts.push(`<div class="city-six-lanterns" data-city-reward="confidence_harbor" data-source-category="extended" aria-label="六念燈景">${['念佛','念法','念僧','念戒','念施','念天'].map((name,i)=>`<i data-recollection="${name}" style="--x:${7+i*3.5}%;--y:${82-Math.sin(i/5*Math.PI)*6}%" title="${name}"></i>`).join('')}</div>`);
 if(f.effort_garden)parts.push(`<div data-city-reward="effort_garden" data-source-category="extended"><img class="city-effort-flowers" src="${asset(CITY_REWARD_SOURCES.garden.path)}" alt="四正勤完成後，既有花草圖層在花園中盛開">${vignette('effort',[270,160,820,650],64,70,11,'四正勤繪本澆灌花園原圖局部')}</div>`);
 if(f.calm_insight_messengers)parts.push('<div class="city-breathing-ripples" data-city-reward="calm_insight_messengers" data-source-category="mixed" aria-label="雙使相伴的安靜呼吸水波"><i></i><i></i><i></i></div>');
 if(f.endeavor_boat)parts.push(`<img class="city-endeavor-boat" data-city-reward="endeavor_boat" data-source-category="extended" src="${asset(CITY_REWARD_SOURCES.boat.path)}" alt="四如意足延伸：既有調心小舟美術">`);
 if(f.jhana_garden)parts.push(`<div class="city-jhana-garden" data-city-reward="jhana_garden" data-source-category="extended" aria-label="四禪的四個既有譬喻">${[[220,195,350,340],[580,195,350,340],[940,195,350,340],[1300,195,350,340]].map((c,i)=>vignette('jhanas',c,[27,38,62,73][i],8,7.5,['澡粉團','湧泉池','蓮花池','白布覆身'][i]+'，四禪原圖局部')).join('')}</div>`);
 parts.push(zoneLinks(s),companions(s));
 if(f.fruition_guide)parts.push(`<div data-city-reward="fruition_guide" data-source-category="extended">${vignette('fruition',[250,120,950,560],91,18,11,'四向四果與十結繪本的繫縛意象局部')}</div>`);
 return `<div class="city-extended-rewards" data-city-extended-layer>${parts.join('')}</div>`;
}
export function renderRewardSourcePreview(id){
 if(id==='awakening_companions')return `<figure class="city-reward-source-preview">${sourceViewport('companions',null,{label:'七覺支既有七位角色總圖'})}<figcaption>既有繪本原圖；城中的念燈仍由同一位念-守門人承接。</figcaption></figure>`;
 if(id==='jhana_garden')return `<figure class="city-reward-source-preview">${sourceViewport('jhanas',[215,190,1440,344],{label:'四禪四個既有譬喻'})}<figcaption>四禪繪本原圖局部</figcaption></figure>`;
 if(id==='effort_garden')return `<figure class="city-reward-source-preview">${sourceViewport('effort',null,{label:'四正勤繪本澆花原圖'})}<figcaption>四正勤繪本原圖</figcaption></figure>`;
 if(id==='noble_path')return `<figure class="city-reward-source-preview">${sourceViewport('wholesome',null,{label:'十善生活既有四格繪本圖'})}<figcaption>八正道與十善業道繪本原圖</figcaption></figure>`;
 return '';
}
