import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatExpansionModule } from '@angular/material/expansion';

@Component({
  selector: 'app-faq',
  standalone: true,
  imports: [CommonModule, MatExpansionModule],
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.css']
})
export class FaqComponent {
  faqs = [
    {
      question: 'How do I view my pension statement?',
      answer: 'Login to your dashboard and navigate to the "Pension Statements" tab.'
    },
    {
      question: 'Can I update my personal information?',
      answer: 'Yes, go to your profile settings and edit your personal details securely.'
    },
    {
      question: 'Is my pension data secure?',
      answer: 'Absolutely. We use MFA, RBAC, and end-to-end encryption.'
    },
    {
      question: 'What should I do if I forget my login credentials?',
      answer: 'Click “Forgot Password” on the login page and follow the instructions to reset your password securely.'
    },
    {
      question: 'Can I upload pension-related documents?',
      answer: 'Yes, the Document Management section lets you upload and securely store pension files for future reference.'
    },
    {
      question: 'How do I switch my pension fund?',
      answer: 'Please contact your pension provider. You can view current fund details in the “Pension Fund” section of your dashboard.'
    },
    {
      question: 'Is there legal support available?',
      answer: 'While we don’t provide legal advice, we link to trusted third-party pension advisory services under the Resources tab.'
    },
    {
      question: 'How do I delete my account?',
      answer: 'Contact support using the email us to request secure account deletion.'
    },
    {
      question: 'How frequently is my pension data updated?',
      answer: 'Contribution and statement data is synced in real-time with your pension provider’s records.'
    },
    {
      question: 'What devices are supported?',
      answer: 'The system works seamlessly across desktops, laptops, tablets, and smartphones.'
    },
    {
      question: 'Does the system support multiple languages?',
      answer: 'Yes. The platform supports multiple languages including English and Hindi for better accessibility.'
    },
    {
      question: 'Is there AI chatbot support for pension questions?',
      answer: 'Yes. A built-in AI assistant can help answer pension-related questions via the dashboard interface.'
    },
    {
      question: 'Can I download pension documents as PDFs?',
      answer: 'Yes. Pension statements and uploaded files can be downloaded in PDF format for offline use.'
    }
  
  
  ];
}
