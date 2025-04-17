import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import AOS from 'aos';

bootstrapApplication(AppComponent, appConfig)
  .then(() => AOS.init())
  .catch((err) => console.error(err));
