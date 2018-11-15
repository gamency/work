
/**
 * 在这里给出对类 BeerSong 的描述。
 * 
 * @作者（你的名字）
 * @版本（一个版本号或者一个日期）
 */
public class BeerSong {


public static void main (String[] args) {
int beerNum = 99;
String word = "bottles";
while (beerNum > 0) {
if (beerNum == 1) {
word = "bottle"; // ڇຕ೟ڦጱ
}
System.out.println(beerNum + " "  + word + " of beer on the wall");
System.out.println(beerNum + " " + word + " of beer.");
System.out.println("Take one down.");
System.out.println("Pass it around.");
beerNum = beerNum - 1;
if (beerNum > 0) {
System.out.println(beerNum + " " + word + " of beer on the wall");
} else {
System.out.println("No more bottles of beer on the wall");
}//else঳ຐ
}

String[] wordListOne = {“24/7”,”multiTier”,”30,000 foot”,”B-to-B”,”win-win”,”frontend”, “web-based”,”pervasive”, “smart”, “sixsigma”,”critical-path”, “dynamic”};
String[] wordListTwo = {“empowered”, “sticky”,
“value-added”, “oriented”, “centric”, “distributed”,
“clustered”, “branded”,”outside-the-box”, “positioned”,
“networked”, “focused”, “leveraged”, “aligned”,
“targeted”, “shared”, “cooperative”, “accelerated”};
String[] wordListThree = {“process”, “tippingpoint”, “solution”, “architecture”, “core competency”,
“strategy”, “mindshare”, “portal”, “space”, “vision”,
“paradigm”, “mission”};
// ऺ໙௅ᅃፇᆶܠณ߲ఁَຍᇕ
int oneLength = wordListOne.length;
int twoLength = wordListTwo.length;
int threeLength = wordListThree.length;
// ׂิໜऐຕጴ
int rand1 = (int) (Math.random() * oneLength);
int rand2 = (int) (Math.random() * twoLength);
int rand3 = (int) (Math.random() * threeLength);
// ፇ؜ࢇጆॆຍᇕ
String phrase = wordListOne[rand1] + “ “ +
wordListTwo[rand2] + “ “ + wordListThree[rand3];
؜๼ //
System.out.println(“What we need is a “ + phrase);
}
} //whileთ঳ຐ࣍
} //main݆঳ຐݛ
}
