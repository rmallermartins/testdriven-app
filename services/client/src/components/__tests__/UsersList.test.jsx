import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UsersList';


const users = [
  {
    'active': true,
    'admin': false,
    'email': 'hermanmu@gmail.com',
    'id': 1,
    'username': 'michael'
  },
  {
    'active': true,
    'admin': false,
    'email': 'michael@mherman.org',
    'id': 2,
    'username': 'michaelherman'
  }
]

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  const table = wrapper.find('table');
  const th = wrapper.find('th');
  const td = wrapper.find('td');

  expect(wrapper.find('h1').get(0).props.children).toBe('All Users');

  expect(table.length).toBe(1);

  expect(wrapper.find('thead').length).toBe(1);
  expect(th.length).toBe(5);
  expect(th.get(0).props.children).toBe('ID');
  expect(th.get(1).props.children).toBe('Email');
  expect(th.get(2).props.children).toBe('Username');
  expect(th.get(3).props.children).toBe('Active');
  expect(th.get(4).props.children).toBe('Admin');

  expect(wrapper.find('tbody').length).toBe(1);
  expect(wrapper.find('tbody > tr').length).toBe(2);
  expect(td.length).toBe(10);
  expect(td.get(0).props.children).toBe(1);
  expect(td.get(1).props.children).toBe('hermanmu@gmail.com');
  expect(td.get(2).props.children).toBe('michael');
  expect(td.get(3).props.children).toBe('true');
  expect(td.get(4).props.children).toBe('false');
});

test('UsersList renderiza um snapshot corretamente', () => {
  const tree = renderer.create(<UsersList users={users}/>);
  expect(tree).toMatchSnapshot();
});
