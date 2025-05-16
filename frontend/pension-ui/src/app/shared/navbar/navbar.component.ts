import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatToolbarModule,
    MatButtonModule,
    MatSelectModule,
    MatOptionModule,
    TranslateModule,
    FormsModule
  ],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  isMenuOpen = false;
  selectedLang = 'en';

  constructor(private translate: TranslateService) {}

  ngOnInit(): void {
    if (typeof window !== 'undefined') {
      const storedLang = localStorage.getItem('preferredLang') || 'en';
      this.selectedLang = storedLang;
      this.translate.setDefaultLang(storedLang);
      this.translate.use(storedLang);
    }
  }

  changeLang(event: Event) {
    const value = (event.target as HTMLSelectElement)?.value;
    if (value) {
      this.selectedLang = value;
      this.translate.use(value);
      localStorage.setItem('preferredLang', value);
    }
  }
}
