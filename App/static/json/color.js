var colorMap = {
  '汉族': '#FFF68F',
  '满族': '#FFE4E1',
  '蒙古族': '#FFC1C1',
  '回族': '#FFA54F',
  '藏族': '#FF7F50',
  '维吾尔族': '#FF4500',
  '苗族': '#FDF5E6',
  '彝族': '#F7F7F7',
  '壮族': '#F0FFFF',
  '布依族': '#EEEE00',
  '侗族': '#EEDFCC',
  '瑶族': '#EEC900',
  '白族': '#EE9A49',
  '土家族': '#EE7621',
  '哈尼族': '#EE3A8C',
  '哈萨克族': '#EAEAEA',
  '傣族': '#DEB887',
  '黎族': '#D9D9D9',
  '傈僳族': '#D1D1D1',
  '佤族': '#CDC9A5',
  '畲族': '#CDB7B5',
  '高山族': '#CD9B1D',
  '拉祜族': '#CD7054',
  '水族': '#CD661D',
  '东乡族': '#CD5B45',
  '纳西族': '#CD1076',
  '景颇族': '#CAFF70',
  '柯尔克孜族': '#C1CDC1',
  '土族': '#BFBFBF',
  '达斡尔族': '#BDB76B',
  '仫佬族': '#BBFFFF',
  '羌族': '#B8B8B8',
  '布朗族': '#B4EEB4',
  '撒拉族': '#B0E2FF',
  '毛南族': '#A9A9A9',
  '仡佬族': '#A4D3EE',
  '锡伯族': '#9F79EE',
  '阿昌族': '#9B30FF',
  '普米族': '#98F5FF',
  '朝鲜族': '#8EE5EE',
  '塔吉克族': '#8B7500',
  '怒族': '#8B5A2B',
  '乌孜别克族': '#8B4789',
  '俄罗斯族': '#8B3626',
  '鄂温克族': '#7FFF00',
  '德昂族': '#7B68EE',
  '保安族': '#778899',
  '裕固族': '#6CA6CD',
  '京族': '#66CD00',
  '塔塔尔族': '#5F9EA0',
  '独龙族': '#556B2F',
  '鄂伦春族': '#66CD00',
  '赫哲族': '#388E8E',
  '门巴族': '#228B22',
  '珞巴族': '#1E90FF',
  '基诺族': '#006400'
};

var province = ["北京", "天津", "上海", "重庆", "河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "海南", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "内蒙古", "广西", "西藏", "宁夏", "新疆", "香港", "澳门", "台湾"];

window.getAllNations = function () {
  var res = [];
  for (var key in colorMap) {
    res.push(key);
  };
  return res;
}


window.getAllProvinceNations = function (nationDistributedInfoSettingArr) {
  var res = [];
  // console.log(nationDistributedInfoSettingArr)
  var nArr = nationDistributedInfoSettingArr.concat([]);
  var allNations = [];
  nArr.forEach(function(ele) {
    ele.data.forEach(function (item) {
      item.nationName = ele.nationName;
    });
    allNations = allNations.concat(ele.data);
  });
  // console.log(allNations);
  for (var i = 0; i < province.length; i++) {
    var provinceInfo = {};
    // console.log(province[i])

    var num = 0;
    var areas = [];
    var nations = [];
    allNations.forEach(function(item) {
      // console.log(item);
      if (item.province.indexOf(province[i]) > -1) {
        num += item.value[2];
        areas.push(item.name);
        if (nations.indexOf(item.nationName) == -1) {
          nations.push(item.nationName);
        }
      };
    });
    // res.push(key);
    provinceInfo.value = num;
    provinceInfo.name = province[i];
    provinceInfo.areas = areas;
    provinceInfo.nations = nations;
    res.push(provinceInfo);
  };
  // console.log(res);
  return res;

}