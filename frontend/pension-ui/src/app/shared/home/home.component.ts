import {
  Component,
  AfterViewInit,
  ElementRef,
  ViewChildren,
  QueryList,
  HostListener,
  Inject,
  OnInit
} from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { RouterModule } from '@angular/router';
import { PLATFORM_ID } from '@angular/core';
import { VoiceflowLoaderService } from './voiceflow-loader.service';
import { TranslateService, TranslateModule } from '@ngx-translate/core';


@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, MatButtonModule, TranslateModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, AfterViewInit {
  numbers: any[] = [];
  testimonials: any[] = [];
  activeIndex = 0;

  public isBrowser = false;
  private intervalId!: ReturnType<typeof setInterval>;
  private touchStartX = 0;

  @ViewChildren('statRef', { read: ElementRef }) statRefs!: QueryList<ElementRef>;

  constructor(
    @Inject(PLATFORM_ID) private platformId: Object,
    private chatbot: VoiceflowLoaderService,
    private translate: TranslateService
  ) {
    this.isBrowser = isPlatformBrowser(platformId);

    this.translate.onLangChange.subscribe(() => {
      this.loadTranslatedContent();
    });
  }

  ngOnInit(): void {
    let preferredLang = 'en';
    if (this.isBrowser) {
      preferredLang = localStorage.getItem('preferredLang') || 'en';
    }

    this.translate.use(preferredLang).subscribe(() => {
      this.loadTranslatedContent();
    });
  }

  ngAfterViewInit(): void {
    if (this.isBrowser) {
      this.chatbot.loadChatbotScript();
      this.startAutoRotate();

      setTimeout(() => {
        this.initCounters();
        this.statRefs.changes.subscribe(() => this.initCounters());
      }, 200);
    }
  }

  private loadTranslatedContent(): void {
    this.translate.get('HOME.NUMBERS').subscribe((data) => {
      const rawNumbers = Array.isArray(data) ? data : [];

      this.numbers = rawNumbers.map(item => ({
        ...item,
        target: parseInt(item.target, 10) || 0
      }));

      if (this.isBrowser) {
        setTimeout(() => {
          this.initCounters();
          this.statRefs.changes.subscribe(() => this.initCounters());
        }, 0);
      }
    });

    this.translate.get('HOME.TESTIMONIALS.LIST').subscribe((data) => {
      this.testimonials = Array.isArray(data) ? data : [];
    });
  }

  private initCounters(): void {
    if (!this.isBrowser || typeof IntersectionObserver === 'undefined') {
      this.statRefs.forEach((ref, i) => {
        const el = ref.nativeElement;
        const endVal = this.numbers[i]?.target || 0;
        el.innerText = endVal.toString();
      });
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target as HTMLElement;
          const i = this.statRefs.toArray().findIndex(ref => ref.nativeElement === el);
          const endVal = this.numbers[i]?.target || 0;
          this.animateValue(el, 0, endVal, 1500);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.1 });

    this.statRefs.forEach(ref => observer.observe(ref.nativeElement));
  }

  private animateValue(el: HTMLElement, start: number, end: number, duration: number): void {
    if (!this.isBrowser || typeof requestAnimationFrame === 'undefined') {
      el.innerText = end.toString();
      return;
    }

    let startTime: number | null = null;

    const step = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      const value = Math.floor(progress * (end - start) + start);
      el.innerText = value.toString();
      if (progress < 1) requestAnimationFrame(step);
    };

    requestAnimationFrame(step);
  }

  private startAutoRotate(): void {
    if (!this.isBrowser) return;
    this.intervalId = setInterval(() => this.next(), 5000);
  }

  next(): void {
    if (this.testimonials.length === 0) return;
    this.activeIndex = (this.activeIndex + 1) % this.testimonials.length;
  }

  prev(): void {
    if (this.testimonials.length === 0) return;
    this.activeIndex = (this.activeIndex - 1 + this.testimonials.length) % this.testimonials.length;
  }

  @HostListener('touchstart', ['$event'])
  onTouchStart(evt: TouchEvent): void {
    if (!this.isBrowser) return;
    this.touchStartX = evt.changedTouches[0].clientX;
  }

  @HostListener('touchend', ['$event'])
  onTouchEnd(evt: TouchEvent): void {
    if (!this.isBrowser) return;
    const diff = evt.changedTouches[0].clientX - this.touchStartX;
    if (Math.abs(diff) > 50) diff > 0 ? this.prev() : this.next();
  }
}
