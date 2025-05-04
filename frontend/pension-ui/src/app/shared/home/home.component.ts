import {
  Component,
  AfterViewInit,
  ElementRef,
  ViewChildren,
  QueryList,
  HostListener,
  Inject
} from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { RouterModule } from '@angular/router';
import { PLATFORM_ID } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, MatButtonModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements AfterViewInit {
  /* ──────────  COUNTER DATA ────────── */
  numbers = [
    {
      target: 95,
      label: 'Client Trust Score',
      desc: 'Users consistently rate us for clarity, security, and ease of use.',
      prefix: '',
      suffix: '%'
    },
    {
      target: 20,
      label: 'Years of Expertise',
      desc: 'Delivering robust pension tools backed by UK financial regulations.',
      prefix: '',
      suffix: '+'
    },
    {
      target: 500,
      label: 'Pension Funds Tracked',
      desc: 'Helping thousands make informed retirement decisions.',
      prefix: '£',
      suffix: 'M+'
    }
  ];

  /* ──────────  TESTIMONIAL DATA ────── */
  testimonials = [
    {
      quote: 'The portal finally gave me a clear picture of my entire pension.',
      name: 'Sarah Collins',
      role: 'Marketing Manager · London'
    },
    {
      quote: 'Secure and incredibly easy to navigate—highly recommended.',
      name: 'Michael Osei',
      role: 'Software Engineer · Manchester'
    },
    {
      quote: 'Love the contribution tracking charts. I feel in control of my future.',
      name: 'Priya Patel',
      role: 'Teacher · Birmingham'
    }
  ];
  activeIndex = 0;
  private intervalId!: ReturnType<typeof setInterval>;
  private touchStartX = 0;

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  /* refs for counters */
  @ViewChildren('statRef') statRefs!: QueryList<ElementRef>;

  /* ──────────  LIFECYCLE  ──────────── */
  ngAfterViewInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.initCounters();
      this.startAutoRotate();
    }
  }

  /* ──────────  COUNTER LOGIC  ──────── */
  private initCounters() {
    const animate = (el: HTMLElement) => {
      const endVal = +el.getAttribute('data-target')!;
      this.animateValue(el, 0, endVal, 1500);
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animate(entry.target as HTMLElement);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 } // lower so tiny visibility triggers
    );

    // kick off immediately in case section is already visible
    this.statRefs.forEach((ref) => {
      animate(ref.nativeElement);
      observer.observe(ref.nativeElement);
    });
  }

  private animateValue(
    el: HTMLElement,
    start: number,
    end: number,
    duration: number
  ) {
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

  /* ──────────  TESTIMONIAL ROTATOR ─── */
  private startAutoRotate() {
    this.intervalId = setInterval(() => this.next(), 5000);
  }

  next() {
    this.activeIndex = (this.activeIndex + 1) % this.testimonials.length;
  }

  prev() {
    this.activeIndex =
      (this.activeIndex - 1 + this.testimonials.length) %
      this.testimonials.length;
  }

  /* ─────  Swipe Support on Mobile  ─── */
  @HostListener('touchstart', ['$event'])
  onTouchStart(evt: TouchEvent) {
    this.touchStartX = evt.changedTouches[0].clientX;
  }

  @HostListener('touchend', ['$event'])
  onTouchEnd(evt: TouchEvent) {
    const diff = evt.changedTouches[0].clientX - this.touchStartX;
    if (Math.abs(diff) > 50) diff > 0 ? this.prev() : this.next();
  }
}
