import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeroBannerComponent } from './hero-banner/hero-banner.component';
import { AboutComponent } from './about/about.component';
import { ServicesComponent } from './services/services.component';
import { TestimonialsComponent } from './testimonials/testimonials.component';
import { BlogPreviewComponent } from './blog-preview/blog-preview.component';
import { FooterComponent } from '../../shared/footer/footer.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, HeroBannerComponent, AboutComponent, ServicesComponent, TestimonialsComponent, BlogPreviewComponent, FooterComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {}

