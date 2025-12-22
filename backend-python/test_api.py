"""
Poly-i Chatbot Backend API 테스트 스크립트

프론트엔드 없이 Python 백엔드 API를 직접 테스트합니다.

사용법:
    python test_api.py
"""

import requests
import json
import time
from typing import Dict, Any


class PolyiAPITester:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()

    def print_header(self, text: str):
        """테스트 섹션 헤더 출력"""
        print("\n" + "="*60)
        print(f"  {text}")
        print("="*60)

    def print_response(self, response: requests.Response):
        """응답 결과 포맷팅 출력"""
        print(f"\n상태 코드: {response.status_code}")
        print(f"응답 시간: {response.elapsed.total_seconds():.2f}초")

        try:
            data = response.json()
            print("\n응답 내용:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        except json.JSONDecodeError:
            print("\n응답 내용 (텍스트):")
            print(response.text)

    def test_health_check(self):
        """서버 헬스 체크"""
        self.print_header("1. 헬스 체크 테스트")

        try:
            response = self.session.get(f"{self.base_url}/health")
            self.print_response(response)

            if response.status_code == 200:
                print("\n✅ 서버가 정상적으로 실행 중입니다!")
                return True
            else:
                print("\n❌ 서버 응답 오류")
                return False
        except requests.exceptions.ConnectionError:
            print("\n❌ 서버에 연결할 수 없습니다!")
            print("   Python 백엔드가 실행 중인지 확인하세요: python app.py")
            return False

    def test_info(self):
        """서버 정보 조회"""
        self.print_header("2. 서버 정보 조회 테스트")

        try:
            response = self.session.get(f"{self.base_url}/info")
            self.print_response(response)
            return response.status_code == 200
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return False

    def test_generate_simple(self):
        """간단한 텍스트 생성 테스트"""
        self.print_header("3. 간단한 질문 테스트")

        payload = {
            "prompt": "안녕하세요",
            "language": "ko",
            "user_id": "test-user-001"
        }

        print(f"\n요청 데이터:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))

        try:
            response = self.session.post(
                f"{self.base_url}/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            self.print_response(response)
            return response.status_code == 200
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return False

    def test_generate_department_info(self):
        """학과 정보 질문 테스트"""
        self.print_header("4. 학과 정보 질문 테스트")

        payload = {
            "prompt": "AI응용소프트웨어학과에 대해 알려줘",
            "language": "ko",
            "user_id": "test-user-001"
        }

        print(f"\n요청 데이터:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))

        try:
            response = self.session.post(
                f"{self.base_url}/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            self.print_response(response)
            return response.status_code == 200
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return False

    def test_generate_employment(self):
        """취업 정보 질문 테스트"""
        self.print_header("5. 취업 정보 질문 테스트")

        payload = {
            "prompt": "취업률이 어떻게 되나요?",
            "language": "ko",
            "user_id": "test-user-001"
        }

        print(f"\n요청 데이터:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))

        try:
            response = self.session.post(
                f"{self.base_url}/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            self.print_response(response)
            return response.status_code == 200
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return False

    def test_generate_facility(self):
        """시설 정보 질문 테스트"""
        self.print_header("6. 시설 정보 질문 테스트")

        payload = {
            "prompt": "식당이나 주차장은 어디에 있나요?",
            "language": "ko",
            "user_id": "test-user-001"
        }

        print(f"\n요청 데이터:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))

        try:
            response = self.session.post(
                f"{self.base_url}/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            self.print_response(response)
            return response.status_code == 200
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return False

    def test_embedding(self):
        """임베딩 생성 테스트"""
        self.print_header("7. 임베딩 생성 테스트")

        payload = {
            "text": "한국폴리텍대학 분당캠퍼스"
        }

        print(f"\n요청 데이터:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))

        try:
            response = self.session.post(
                f"{self.base_url}/embed",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            print(f"\n상태 코드: {response.status_code}")
            print(f"응답 시간: {response.elapsed.total_seconds():.2f}초")

            if response.status_code == 200:
                data = response.json()
                print(f"\n임베딩 차원: {data.get('dimension', 'N/A')}")
                print(f"모델: {data.get('model', 'N/A')}")

                embedding = data.get('embedding', [])
                if embedding:
                    print(f"임베딩 벡터 (처음 10개): {embedding[:10]}")
                    print("✅ 임베딩 생성 성공!")
                return True
            else:
                print(f"\n❌ 임베딩 생성 실패")
                return False
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return False

    def test_english_query(self):
        """영어 질문 테스트"""
        self.print_header("8. 영어 질문 테스트")

        payload = {
            "prompt": "Tell me about the AI department",
            "language": "en",
            "user_id": "test-user-001"
        }

        print(f"\n요청 데이터:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))

        try:
            response = self.session.post(
                f"{self.base_url}/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            self.print_response(response)
            return response.status_code == 200
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return False

    def run_all_tests(self):
        """모든 테스트 실행"""
        print("\n" + "🚀 "*20)
        print("  Poly-i Chatbot Backend API 테스트 시작")
        print("🚀 "*20)

        results = []

        # 헬스 체크 먼저 실행
        health_ok = self.test_health_check()
        if not health_ok:
            print("\n❌ 서버가 실행되지 않았습니다. 테스트를 종료합니다.")
            print("\n실행 방법:")
            print("  cd backend-python")
            print("  python app.py")
            return

        results.append(("헬스 체크", health_ok))

        # 나머지 테스트 실행
        time.sleep(1)
        results.append(("서버 정보", self.test_info()))

        time.sleep(1)
        results.append(("간단한 질문", self.test_generate_simple()))

        time.sleep(1)
        results.append(("학과 정보", self.test_generate_department_info()))

        time.sleep(1)
        results.append(("취업 정보", self.test_generate_employment()))

        time.sleep(1)
        results.append(("시설 정보", self.test_generate_facility()))

        time.sleep(1)
        results.append(("임베딩 생성", self.test_embedding()))

        time.sleep(1)
        results.append(("영어 질문", self.test_english_query()))

        # 결과 요약
        self.print_header("테스트 결과 요약")

        passed = sum(1 for _, result in results if result)
        total = len(results)

        print(f"\n총 {total}개 테스트 중 {passed}개 통과\n")

        for test_name, result in results:
            status = "✅ 통과" if result else "❌ 실패"
            print(f"  {status}  {test_name}")

        print("\n" + "="*60)

        if passed == total:
            print("🎉 모든 테스트가 성공적으로 완료되었습니다!")
        else:
            print(f"⚠️  {total - passed}개의 테스트가 실패했습니다.")

        print("="*60 + "\n")


def interactive_mode():
    """대화형 모드"""
    print("\n" + "💬 "*20)
    print("  대화형 테스트 모드")
    print("💬 "*20)
    print("\n명령어:")
    print("  - 'quit' 또는 'exit': 종료")
    print("  - 'clear': 화면 지우기")
    print("  - 그 외: 챗봇에게 질문\n")

    base_url = "http://localhost:5001"
    session = requests.Session()

    while True:
        try:
            user_input = input("\n🙋 질문: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', '종료']:
                print("\n👋 테스트를 종료합니다.")
                break

            if user_input.lower() == 'clear':
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                continue

            # API 호출
            payload = {
                "prompt": user_input,
                "language": "ko",
                "user_id": "interactive-user"
            }

            print("\n⏳ 응답 생성 중...")
            start_time = time.time()

            response = session.post(
                f"{base_url}/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            elapsed = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                answer = data.get('response', '응답 없음')
                source = data.get('source', 'unknown')

                print(f"\n🤖 Poly-i: {answer}")
                print(f"\n📊 응답 시간: {elapsed:.2f}초 | 소스: {source}")
            else:
                print(f"\n❌ 오류 발생: {response.status_code}")
                print(response.text)

        except KeyboardInterrupt:
            print("\n\n👋 테스트를 종료합니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류: {e}")


if __name__ == "__main__":
    import sys

    print("""
╔══════════════════════════════════════════════════════════╗
║   Poly-i Chatbot Backend API 테스트 도구                ║
║   한국폴리텍대학 분당캠퍼스                              ║
╚══════════════════════════════════════════════════════════╝
    """)

    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        interactive_mode()
    else:
        print("\n실행 모드:")
        print("  1. 자동 테스트 (현재)")
        print("  2. 대화형 모드: python test_api.py interactive\n")

        tester = PolyiAPITester()
        tester.run_all_tests()

        print("\n💡 대화형 모드로 전환하시겠습니까? (y/n): ", end='')
        choice = input().strip().lower()

        if choice in ['y', 'yes', '예']:
            interactive_mode()