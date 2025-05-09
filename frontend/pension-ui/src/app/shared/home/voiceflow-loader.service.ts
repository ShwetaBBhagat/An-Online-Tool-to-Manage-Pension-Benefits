import { Injectable } from '@angular/core';
declare global {
    interface Window {
      voiceflow: {
        chat: {
          load: (config: {
            verify: { projectID: string };
            url: string;
            versionID: string;
            voice?: { url: string };
          }) => void;
        };
      };
    }
  }
  
@Injectable({ providedIn: 'root' })
export class VoiceflowLoaderService {
  private scriptLoaded = false;

  loadChatbotScript() {
    if (this.scriptLoaded) return; // Prevent reloading if already loaded
    console.log('[TED] Loading chatbot script...');

    const script = document.createElement('script');
    script.src = 'https://cdn.voiceflow.com/widget-next/bundle.mjs';
    script.type = 'text/javascript';
    script.onload = () => {
      window.voiceflow.chat.load({
        verify: { projectID: '681c93dfdbdfd7143481962b' },
        url: 'https://general-runtime.voiceflow.com',
        versionID: 'production',
        voice: {
          url: "https://runtime-api.voiceflow.com"
        }
      });
    };

    document.body.appendChild(script);
    this.scriptLoaded = true;
  }
}
