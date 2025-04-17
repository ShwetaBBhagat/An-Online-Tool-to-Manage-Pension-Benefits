import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-testimonials',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './testimonials.component.html',
  styleUrls: ['./testimonials.component.css']
})
export class TestimonialsComponent {
  testimonials = [
    {
      name: 'Anita Sharma',
      photo: 'https://randomuser.me/api/portraits/women/68.jpg',
      quote: 'PensionPortal made it incredibly easy to understand and manage my retirement contributions.',
      rating: 5
    },
    {
      name: 'David Patel',
      photo: 'https://randomuser.me/api/portraits/men/52.jpg',
      quote: 'As an employer, I love how seamless the platform is to manage staff pensions.',
      rating: 4
    },
    {
      name: 'Priya Kapoor',
      photo: 'https://randomuser.me/api/portraits/women/22.jpg',
      quote: 'The user dashboard is so intuitive. I check my pension progress every month!',
      rating: 5
    }
  ];
}
