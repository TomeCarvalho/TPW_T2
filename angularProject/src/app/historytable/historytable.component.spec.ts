import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistorytableComponent } from './historytable.component';

describe('HistorytableComponent', () => {
  let component: HistorytableComponent;
  let fixture: ComponentFixture<HistorytableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HistorytableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HistorytableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
