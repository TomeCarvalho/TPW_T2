import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-historytable',
  templateUrl: './historytable.component.html',
  styleUrls: ['./historytable.component.css']
})
export class HistorytableComponent implements OnInit {

  @Input() data: any;
  @Input() type!: string;

  constructor() { }

  ngOnInit(): void {

  }

}
