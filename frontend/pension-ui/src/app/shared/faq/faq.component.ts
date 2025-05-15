import { Component, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { TranslateService, TranslateModule } from '@ngx-translate/core';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-faq',
  standalone: true,
  imports: [CommonModule, MatExpansionModule, TranslateModule, MatProgressSpinnerModule],
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.css']
})
export class FaqComponent implements OnInit {
  faqs: { question: string; answer: string }[] = [];
  loading = true;
  private isBrowser: boolean;

  constructor(
    @Inject(PLATFORM_ID) private platformId: Object,
    private translate: TranslateService
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
  }

  ngOnInit(): void {
    this.loadFaqs();
    this.translate.onLangChange.subscribe(() => this.loadFaqs());
  }

  private loadFaqs(): void {
    this.loading = true;
    this.translate.get('FAQ.LIST').subscribe((data: any) => {
      if (Array.isArray(data)) {
        this.faqs = data;
      } else {
        console.warn('FAQ.LIST is not an array or missing in translation file.');
        this.faqs = [];
      }
      this.loading = false;
    });
  }
}
