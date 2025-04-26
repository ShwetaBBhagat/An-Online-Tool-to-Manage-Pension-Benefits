import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-view-employer-documents',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './view-documents.component.html',
  styleUrls: ['./view-documents.component.css']
})
export class ViewEmployerDocumentsComponent {
  documents: any[] = [];
  errorMsg = '';

  constructor(private http: HttpClient) {
    this.fetchDocuments();
  }

  fetchDocuments() {
    const token = localStorage.getItem('employerToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.get<any>('http://127.0.0.1:5000/api/employer/documents', { headers }).subscribe({
      next: (res) => {
        this.documents = res.documents || [];
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Failed to load documents.';
      }
    });
  }
}
