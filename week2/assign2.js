// Task 1
function func1(name) {
  let characters = {
    悟空: { x: 0, y: 0, z: 1 },
    丁滿: { x: -1, y: 4, z: -1 },
    辛巴: { x: -3, y: 3, z: 1 },
    貝吉塔: { x: -4, y: -1, z: 1 },
    特南克斯: { x: 1, y: -2, z: 1 },
    弗利沙: { x: 4, y: -1, z: -1 },
    distance: function (name1, name2) {
      let a = this[name1];
      let b = this[name2];
      let result = Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
      if (a.z != b.z) {
        result += 2;
      }
      return result;
    },
  };

  let list = Object.keys(characters);
  let distarr = [];

  for (let i = 0; i < list.length; i++) {
    if (list[i] != name && list[i] !== "distance") {
      let d = characters.distance(name, list[i]);
      distarr.push({ name: list[i], distance: d });
    }
  }

  let maxdist = Math.max(...distarr.map((e) => e.distance));
  let farthest = distarr.filter((e) => e.distance == maxdist);
  console.log(
    "最遠：",
    farthest.map((e) => e.name)
  );

  let mindist = Math.min(...distarr.map((e) => e.distance));
  let nearest = distarr.filter((e) => e.distance == mindist);
  console.log(
    "最近：",
    nearest.map((e) => e.name)
  );
}

func1("辛巴");
func1("悟空");
func1("弗利沙");
func1("特南克斯");

// Task 2
let booked = []; //預定狀態數列
function isOverlap(start1, end1, start2, end2) {
  return start1 < end2 && start2 < end1;
} // 判斷是否重疊

function isAvailable(s, start, end) {
  return !booked.some(
    //達成任一條件回傳!true=false
    (b) =>
      b.name == s.name && // 同一個人
      b.available === false && //不可以預約的
      isOverlap(b.start, b.end, start, end) //時間有重疊
  );
}

function func2(ss, start, end, criteria) {
  let field;
  let value;
  let op;

  if (criteria.includes(">=")) {
    //拆開字串和=.<=.>=
    [field, value] = criteria.split(">=");
    op = ">=";
  } else if (criteria.includes("<=")) {
    [field, value] = criteria.split("<=");
    op = "<=";
  } else if (criteria.includes("=")) {
    [field, value] = criteria.split("=");
    op = "=";
  }
  if (field != "name") {
    value = Number(value); //字串轉數字
  }
  // console.log([field, value]);

  let candidates = []; //候選人數列

  for (let s of ss) {
    if (op == ">=" && s[field] >= value) {
      candidates.push(s);
    }
    if (op == "=" && s[field] == value) {
      candidates.push(s);
    }
    if (op == "<=" && s[field] <= value) {
      candidates.push(s);
    }
  }

  let free = candidates.filter((s) => isAvailable(s, start, end)); //放入函式篩選可以服務的

  if (free.length == 0) {
    console.log("Sorry");
    return;
  } else if (free.length == 1) {
    console.log(free[0].name);
    booked.push({
      name: free[0].name,
      start: start,
      end: end,
      available: false, //回傳預定狀態
    });
    return;
  } else if (free.length > 1) {
    let diffs = free.map((s) => Math.abs(s[field] - value));
    let mindiff = Math.min(...diffs);
    let best = free[diffs.indexOf(mindiff)];
    console.log(best.name);
    booked.push({
      name: best.name,
      start: start,
      end: end,
      available: false, //回傳預定狀態
    });
  }
}

const services = [
  { name: "S1", r: 4.5, c: 1000 },
  { name: "S2", r: 3, c: 1200 },
  { name: "S3", r: 3.8, c: 800 },
];

func2(services, 15, 17, "c>=800"); // S3
func2(services, 11, 13, "r<=4"); // S3
func2(services, 10, 12, "name=S3"); // Sorry
func2(services, 15, 18, "r>=4.5"); // S1
func2(services, 16, 18, "r>=4"); // Sorry
func2(services, 13, 17, "name=S1"); // Sorry
func2(services, 8, 9, "c<=1500"); // S2

// Task 3
// let seq = [25, 23, 20, 21, 23, 21, 18, 19, 21, 19, 16, 17];
// for (let k = 1; k < seq.length; k++) {
//   console.log(seq[k] - seq[k - 1]);
// }

function func3(index) {
  let addarr = [-2, -3, 1, 2];
  let value = 25;

  for (let n = 0; n < index; n++) {
    value += addarr[n % addarr.length];
  }

  console.log(value);
}

func3(1);
func3(5);
func3(10);
func3(30);

// Task 4
function func4(sp, stat, n) {
  let minusarr = [];
  for (let i = 0; i < sp.length; i++) {
    if (stat[i] == "0" && sp[i] >= n) {
      minusarr.push({ index: i, seat: sp[i] - n });
    }
  }

  if (minusarr.length > 0) {
    let min = Math.min(...minusarr.map((e) => e.seat));
    let bestcar = minusarr.filter((e) => e.seat == min);
    console.log(bestcar[0].index);
  } else {
    let fallbackarr = [];
    for (let i = 0; i < sp.length; i++) {
      if (stat[i] == "0") {
        fallbackarr.push({ index: i, seat: sp[i] });
      }
    }
    let max = Math.max(...fallbackarr.map((e) => e.seat));
    let bestcar = fallbackarr.filter((e) => e.seat == max);
    console.log(bestcar[0].index);
  }
}

func4([3, 1, 5, 4, 3, 2], "101000", 2);
func4([1, 0, 5, 1, 3], "10100", 4);
func4([4, 6, 5, 8], "1000", 4);
