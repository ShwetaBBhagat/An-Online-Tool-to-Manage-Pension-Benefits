import { Component, OnInit } from '@angular/core';
import { ApiService } from './services/api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'pension-tool';
  backendMessage: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.apiService.testBackend().subscribe(
      (response: any) => {
        this.backendMessage = response.message;
        console.log('Backend Response:', response);
      },
      (error: any) => {  // Explicitly define 'error' type
        this.backendMessage = 'Backend connection failed!';
        console.error('API Error:', error);
      }
    );
  }
}
