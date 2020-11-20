# Unifox Python Tetris

## Abstract

우리는 만든다.. ㅔㅌ트리스!!

바로 시작한다.

## What is tetris

https://namu.wiki/w/%ED%85%8C%ED%8A%B8%EB%A6%AC%EC%8A%A4

## Characteristic

1. 10 X 20 의 grid로 이루어져있다.
2. 한 줄이 가득 차면 해당 줄이 삭제되고, 점수가 증가한다. 또한 위의 블럭들이 한칸씩 내려온다.
3. 블럭은 7가지 (I,O,Z,S,J,L,T)로 되어있으며, 3가지의  패턴이 반복해서 나온다. [1]
4. 블럭은 회전, 낙하, 즉시 낙하(?), 홀드가 가능하다.
5. 블럭은 일정 시간이 지나면 자동으로 내려간다.
6. 블럭을 깰수록 속도가 빨라진다.
7. 블럭이 맨 윗칸까지 가득 차면 game over이다.

+블럭 높이에 따라 점수가 증가한다.

[1] 7종의 미노가 한 묶음으로 나온다. 즉, 처음 나오는 7개 미노를 보면 중복되는 미노가 없다. 이 한 묶음을 가방이라고 부르는 데, 1묶음은 1번 가방, 2묶음은 2번 가방으로 부른다. 그렇게 3번 가방까지 나온 후로는 **여태까지 나온 순서 그대로 반복되서 나온다.** 즉, (1번 가방 O, L, J, S, I, Z, T), (2번 가방 J, I, T, L, S, Z, O), (3번 가방 I, O, T, Z, J, S, L) 이렇게 나오면 완전 똑같이 (4번 가방 O, L, J, S, I, Z, T), (5번 가방 J, I, T, L, S, Z, O), (6번 가방 I, O, T, Z, J, S, L) 이렇게 반복한다는 거다.

## pygame?

pygame은 python을 이용하여 display와 event 처리를 해주는 좋은 module이다.

pygame은 다음과 같이 설치할 수 있다.

```
conda create -n tetris python=3.6
pip install pygame
```

## to make

1. display and key event
2. apply tetris rule and system

## Class

크게 2 가지로 나누자.


### (1) BlockSet

BlockSet은 아래와 같은 블록들의 위치와 색들을 저장하는 class 로 선언한다.

BlockSet Class에서는 다음과 같은 method를 정의한다.(= 다음의 역할을 할줄 알아야한다.)

#### isTetris()

줄 삭제(이하 테트리스)가 되었는지 확인하고 획득 점수를 return 해주는 method.

##### return

score(int)

#### isGameOver()

블럭이 가득 차서 게임이 종료되었는지 확인한다.

##### return

gameover(bool)



### (2) Block

개별 블록의 모양과 색, 위치 등을 저장하는 class이다.

#### __ init __(blocktype)

생성자, 변수의 초기화

##### parameter:

blocktype(int) 블럭의 종류를 정의한다.

#### leftTurn()

왼쪽으로 회전한다.

####rightTurn()

오른쪽으로 회전한다.

#### crash()

해당 Block과 BlockSet이 충돌했는지 확인한다.

충돌 하였으면, 해당 블록의 모양을 BlockSet의 모양에 추가한다. 색도 마찬가지



### Game (3)

메인 클래스, 게임의 시작, 종료, input output 등등 플레이어와의 상호작용을 담당한다.

#### init()

각종 변수를 초기화한다. (게임 재시작을 위하여)

#### setBag()

랜덤 난수를 이용하여 반복할 가방의 패턴을 생성한다.

#### step()

한 턴을 진행한다. 사용자의 입력, 계산등이 포함된다.

#### render()

현재 step의 status를 rendering 해준다.



### now, Lets do this!

