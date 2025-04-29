import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-user-documents',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './user-documents.component.html',
  styleUrls: ['./user-documents.component.css']
})
export class UserDocumentsComponent {
  documents: any[] = [];

  constructor(private http: HttpClient) {
    this.loadDocuments();
  }

  loadDocuments() {
    const token = localStorage.getItem('userToken');

    if (!token) {
      console.error('No token found');
      return;
    }

    this.http.get<any>('http://127.0.0.1:5000/api/auth/user/documents', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).subscribe({
      next: (res) => {
        this.documents = res.documents;
      },
      error: (err) => {
        console.error('Error fetching documents:', err);
      }
    });
  }

  viewDocument(docId: number) {
    const token = localStorage.getItem('userToken');
    const url = `http://127.0.0.1:5000/api/auth/user/documents/${docId}/view?token=${token}`;
    window.open(url, '_blank');
  }

  downloadDocument(docId: number, filename: string) {
    const token = localStorage.getItem('userToken');

    this.http.get(`http://127.0.0.1:5000/api/auth/user/documents/${docId}/download`, {
      headers: {
        Authorization: `Bearer ${token}`
      },
      responseType: 'blob'
    }).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: (err) => {
        console.error('Error downloading document:', err);
      }
    });
  }
}
