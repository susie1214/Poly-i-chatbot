import '@/styles/iphone.css';
import { useEffect } from 'react';
import IPhoneFrame from '@/components/IPhoneFrame';
import ChatContainer from '@/components/ChatContainer';
import homepageBg from '@/assets/homepage.png';

function App() {
  useEffect(() => {
    document.documentElement.style.scrollBehavior = 'smooth';
  }, []);

  return (
    <div
      className="min-h-screen flex items-center justify-end p-4 md:pr-10 bg-center bg-no-repeat bg-cover"
      style={{ backgroundImage: `url(${homepageBg})` }}
    >
      <IPhoneFrame>
        <ChatContainer />
      </IPhoneFrame>
    </div>
  );
}

export default App;
