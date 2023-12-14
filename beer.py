import streamlit as st
import openai
import os

# OpenAI API 키 설정
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']


def recommend_beer(selected_intensity, selected_calories, selected_flavor, selected_origin, selected_malt, selected_variety):
    # 맥주 목록 가져오기
    beers = get_beer_list()

    # 사용자가 선택한 조건에 맞게 맥주 추천
    filtered_beers = [beer for beer in beers
                      if beer["알코올도수"] == selected_intensity
                      and beer["칼로리"] == selected_calories
                      and beer["맛"] == selected_flavor
                      and beer["생산지"] == selected_origin
                      and beer["맥아"] == selected_malt
                      and beer["종류"] == selected_variety]
                
    # 조건에 맞는 맥주가 없을 때 OpenAI로 추천 생성
    if not filtered_beers:
        # 기본적인 프롬프트
        prompt = "맥주 추천:"

        # 선택된 조건들을 추가
        prompt += f" 알코올도수 {selected_intensity}, 칼로리 {selected_calories}, 맛 {selected_flavor}, 생산지 {selected_origin}, 맥아 {selected_malt}, 종류 {selected_variety}"

        # 전체 맥주 목록에서 'name' 정보를 추가
        prompt += " ".join([beer["name"] for beer in beers])

        # OpenAI에 prompt 전달
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )

        # OpenAI에서 생성된 텍스트 추천 반환
        recommended_text = response.choices[0].text.strip()

        # 추천된 텍스트를 맥주 리스트에서 가져오기
        recommended_beer = next((beer for beer in beers if beer["name"] in recommended_text), None)

        # 추천된 맥주가 있으면 반환, 없으면 기본 메시지 반환
        if recommended_beer:
            return f"{recommended_beer['name']}를 추천합니다!"
        else:
            return "죄송합니다. 추천할 맥주를 찾지 못했습니다."

    else:
        # 조건에 맞는 맥주가 있을 때는 무작위로 선택하여 "~~맥주를 추천합니다"로 반환
        recommended_beer = filtered_beers[0]
        return f"{recommended_beer['name']}를 추천합니다!"



def get_beer_list():
    # 맥주 목록
    beers = [
    {"name": "덕덕 구스", "알코올도수": "있음", "칼로리": "보통", "맥아": "라이","맛": "쓴 맛","종류": "크래프트", "생산지": "미국"},
    {"name": "구스 IPA", "알코올도수": "있음", "칼로리": "낮음", "맥아": "라이","맛": "깔끔한 맛","종류": "람빅", "생산지": "미국"},
    {"name": "홉 하우스", "알코올도수": "있음", "맥아": "보리", "맛": "쓴맛", "종류": "에일", "칼로리": "보통", "생산지": "네덜란드"},
    {"name": "빅 웨이브", "알코올도수": "있음", "맥아": "라이", "맛": "풍미로운 맛", "종류": "라거", "칼로리": "높음", "생산지": "미국"},
    {"name": "블랑 1663", "알코올도수": "있음", "칼로리": "높음", "맥아": "밀","맛": "깔끔한 맛","종류": "에일", "생산지": "폴란드"},
    {"name": "하이네켄", "알코올도수": "있음", "맥아": "보리", "맛": "깔끔한 맛", "종류": "에일", "칼로리": "낮음", "생산지": "네덜란드"},
    {"name": "카스", "알코올도수": "있음", "맥아": "보리", "맛": "상쾌한 맛", "종류": "라거", "칼로리": "낮음", "생산지": "대한민국"},
    {"name": "호가든", "알코올도수": "있음", "맥아": "밀", "맛": "고소한 맛", "종류": "에일", "칼로리": "높음", "생산지": "벨기에"},
    {"name": "테라", "알코올도수": "있음", "맥아": "보리", "맛": "깔끔한 맛", "종류": "라거", "칼로리": "높음", "생산지": "대한민국"},
    {"name": "삿포로", "알코올도수": "있음", "맥아": "보리", "맛": "깔끔한 맛", "종류": "라거", "칼로리": "낮음", "생산지": "일본"},
    {"name": "버드와이저", "알코올도수": "있음", "종류": "라거", "맛": "고소한 맛", "칼로리": "낮음", "맥아": "보리", "생산지": "미국"},
    {"name": "스텔라", "알코올도수": "있음", "맥아": "밀", "맛": "고급스러운 맛", "종류": "라거", "칼로리": "낮음", "생산지": "벨기에"},
    {"name": "기네스 드래프트", "알코올도수": "있음", "종류": "드래프트", "맛": "고소한 맛", "칼로리": "낮음", "맥아": "보리", "생산지": "네덜란드"},
    {"name": "곰표", "알코올도수": "있음", "종류": "라거", "맛": "깔끔한 맛", "맥아": "밀", "칼로리": "낮음", "생산지": "대한민국"},
    {"name": "바이젠슈테판", "알코올도수": "있음", "맥아": "밀", "맛": "고급스러운 맛", "종류": "에일", "칼로리": "낮음", "생산지": "독일"},
    {"name": "벡스", "알코올도수": "있음", "칼로리": "보통", "맛": "깔끔한 맛", "종류": "라거", "맥아": "보리", "생산지": "독일", "생산지": "독일"},
    {"name": "파울라너", "알코올도수": "있음", "칼로리": "보통", "맛": "쓴맛", "종류": "에일", "맥아": "밀", "생산지": "독일"},
    {"name": "오리온", "알코올도수": "있음", "칼로리": "높음", "맛": "시원한 맛", "종류": "라거", "맥아": "보리", "생산지": "일본"},
    {"name": "켈리", "알코올도수": "있음", "맥아": "보리", "맛": "깔끔한 맛", "종류": "라거", "칼로리": "높음", "생산지": "대한민국"},
    {"name": "클라우드", "알코올도수": "있음", "맥아": "보리", "맛": "풍미로운 맛", "종류": "크래프트", "칼로리": "높음", "생산지": "대한민국"},
    {"name": "한맥", "알코올도수": "있음", "맥아": "보리", "맛": "고소한 맛", "종류": "람빅", "칼로리": "높음", "생산지": "대한민국"},
    {"name": "맥스", "알코올도수": "있음", "맥아": "보리", "맛": "쓴맛", "종류": "람빅", "칼로리": "높음" , "생산지": "대한민국"},
    {"name": "바바리아", "알코올도수": "없음", "맥아": "보리", "맛": "상쾌한 맛", "종류": "람빅", "칼로리": "높음", "생산지": "벨기에"},
    {"name": "투 루츠", "알코올도수": "없음", "맥아": "라이", "맛": "고급스러운맛", "종류": "에일", "칼로리": "높음", "생산지": "폴란드"},
    {"name": "웨팅어 프라이", "알코올도수": "없음", "맥아": "밀", "맛": "고소한 맛", "종류": "라거", "칼로리": "보통", "생산지": "네덜란드"},
    {"name": "하이네켄 제로", "알코올도수": "없음", "맥아": "보리", "맛": "풍미로운 맛", "종류": "라거", "칼로리": "낮음", "생산지": "미국"},
    {"name": "클라우드 클리어 제로", "알코올도수": "없음", "맥아": "보리", "맛": "고소한 맛", "종류": "드래프트", "칼로리": "보통", "생산지": "대한민국"},
    {"name": "하이트 제로", "알코올도수": "없음", "맥아": "라이", "맛": "상쾌한 맛", "종류": "에일", "칼로리": "낮음", "생산지": "대한민국"},
    {"name": "제주 누보", "알코올도수": "없음", "맥아": "보리", "맛": "깔끔한 맛", "종류": "에일", "칼로리": "낮음", "생산지": "대한민국"},
    {"name": "꾸꼬 논알콜", "알코올도수": "없음", "맥아": "밀", "맛": "풍미로운 맛", "종류": "라거", "칼로리": "보통", "생산지": "독일"},
    {"name": "호가든 제로", "알코올도수": "없음", "맥아": "라이", "맛": "시원한 맛", "종류": "람빅", "칼로리": "높음", "생산지": "폴란드"},
    {"name": "카스 제로", "알코올도수": "없음", "맥아": "보리", "맛": "상쾌한 맛", "종류": "크래프트", "칼로리": "보통", "생산지": "대한민국"},
    {"name": "코젤 다크 논알콜", "알코올도수": "없음", "맥아": "밀", "맛": "고급스러운 맛", "종류": "라거", "칼로리": "높음", "생산지": "독일"},
    {"name": "에딩거 프라이", "알코올도수": "없음", "맥아": "보리", "맛": "고소한 맛", "종류": "크래프트", "칼로리": "낮음", "생산지": "네덜란드"},
    {"name": "칭따오 논알콜릭", "알코올도수": "없음", "맥아": "보리", "맛": "쓴맛", "종류": "라거", "칼로리": "낮음", "생산지": "중국"},
    {"name": "클라우스 탈러 오리지널", "알코올도수": "없음", "맥아": "보리", "맛": "쓴맛", "종류": "라거", "칼로리": "낮음", "생산지":"독일"},
    {"name": "그롤쉬 논알콜릭", "알코올도수": "없음", "맥아": "보리", "맛": "깔끔한 맛", "종류": "라거", "칼로리": "낮음", "생산지": "네덜란드"},
    {"name": "크롬바커 바이젠", "알코올도수": "없음", "맥아": "밀", "맛": "고소한 맛", "종류": "라거", "칼로리": "낮음", "생산지": "독일"},
    {"name": "바르슈타이너 프레쉬", "알코올도수": "없음", "맥아": "보리", "맛": "쓴맛", "종류": "라거", "칼로리": "낮음", "생산지": "독일"},
    {"name": "비트버거 드라이브", "알코올도수": "없음", "맥아": "보리", "맛": "쓴맛", "종류": "라거", "칼로리": "낮음", "생산지": "독일"}
    ]
    return beers

def main():
    st.title("맥주 추천 앱")

    # 사용자 입력값 받기
    알코올도수 = st.selectbox("알코올도수", ["있음", "없음"])
    맥아 = st.selectbox("맥아", ["보리", "밀", "라이"])
    종류 = st.selectbox("종류", ["에일", "라거", "람빅", "크래프트"])
    칼로리 = st.selectbox("칼로리", ["낮음", "보통", "높음"])
    맛 = st.selectbox("맛", ["쓴맛", "깔끔한 맛", "고소한 맛", "상쾌한 맛", "고급스러운 맛", "풍미로운 맛", "시원한 맛"])
    생산지 = st.selectbox("생산지", ["한국", "미국", "독일", "폴란드", "벨기에", "일본", "네덜란드"])

    if st.button('시작'):
        recommendbeer = recommend_beer(알코올도수, 칼로리, 맥아 , 종류 , 맛, 생산지)
        st.subheader('추천 맥주')
        st.write(recommendbeer)

if __name__ == "__main__":
    main()