import { Component } from '@angular/core';
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
export class NavbarComponent {
  isMenuOpen = false;
  selectedLang = 'en';

  constructor(private translate: TranslateService) {
    if (typeof window !== 'undefined') {
      const storedLang = localStorage.getItem('preferredLang');
      this.selectedLang = storedLang ? storedLang : 'en';
      this.translate.setDefaultLang(this.selectedLang);
      this.translate.use(this.selectedLang);
    }
  }
changeLang(event: Event) {
  const value = (event.target as HTMLSelectElement)?.value;
  if (value) {
    this.translate.use(value);
    localStorage.setItem('lang', value);
  }
}

}
