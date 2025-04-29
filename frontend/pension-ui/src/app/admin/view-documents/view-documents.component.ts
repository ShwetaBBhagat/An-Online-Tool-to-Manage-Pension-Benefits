import { Component } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-view-documents',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './view-documents.component.html',
  styleUrls: ['./view-documents.component.css']
})
export class ViewDocumentsComponent {
  documents: any[] = [];
  email = '';
  userId: number | null = null;
  startDate = '';
  endDate = '';

  constructor(private http: HttpClient) {
    this.fetchDocuments();
  }

  fetchDocuments() {
    const token = localStorage.getItem('adminToken');
    if (!token) return;

    let params = new HttpParams();
    if (this.email) params = params.set('email', this.email);
    if (this.userId) params = params.set('user_id', this.userId.toString());
    if (this.startDate) params = params.set('start', this.startDate);
    if (this.endDate) params = params.set('end', this.endDate);

    this.http.get<any>('http://127.0.0.1:5000/api/admin/documents', {
      headers: { Authorization: `Bearer ${token}` },
      params
    }).subscribe({
      next: (res) => {
        this.documents = res.documents || [];
      },
      error: (err) => {
        console.error('Error fetching documents:', err);
      }
    });
  }

  viewDocument(documentId: number) {
    const token = localStorage.getItem('adminToken');
    if (!token) return;

    const viewUrl = `http://127.0.0.1:5000/api/admin/documents/${documentId}/view?token=${token}`;
    window.open(viewUrl, '_blank');
  }

  downloadDocument(documentId: number, filename: string) {
    const token = localStorage.getItem('adminToken');
    if (!token) return;

    const downloadUrl = `http://127.0.0.1:5000/api/admin/documents/${documentId}/download?token=${token}`;

    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename;
    link.target = '_blank';
    link.click();
  }
}
