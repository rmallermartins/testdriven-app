import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UsersList';


const users = [
  {
    'active': true,
    'email': 'hermanmu@gmail.com',
    'id': 1,
    'username': 'michael'
  },
  {
    'active': true,
    'email': 'michael@mherman.org',
    'id': 2,
    'username': 'michaelherman'
  }
]

test('UsersList renderiza corretamente', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('michael');
});

test('UsersList renderiza um snapshot corretamente', () => {
  const tree = renderer.create(<UsersList users={users}/>);
  expect(tree).toMatchSnapshot();
});
