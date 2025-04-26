import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-view-documents',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './view-documents.component.html',
  styleUrls: ['./view-documents.component.css']
})
export class ViewDocumentsComponent {
  documents: any[] = [];

  // Filters
  userId = '';
  email = '';
  startDate = '';
  endDate = '';

  constructor(private http: HttpClient, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      if (params['user_id']) this.userId = params['user_id'];
      this.fetchDocuments();
    });
  }  

  fetchDocuments() {
    const token = localStorage.getItem('adminToken');
    const headers = { Authorization: `Bearer ${token}` };

    const params: any = {};
    if (this.userId) params.user_id = this.userId;
    if (this.email) params.email = this.email;
    if (this.startDate) params.start = this.startDate;
    if (this.endDate) params.end = this.endDate;

    this.http.get<any>('http://127.0.0.1:5000/api/admin/documents', { headers, params }).subscribe({
      next: (res) => {
        this.documents = res.documents || [];
      },
      error: (err) => {
        console.error('Error fetching documents:', err);
      }
    });
  }
  
}
