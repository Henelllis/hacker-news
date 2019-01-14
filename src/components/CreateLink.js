import React, { Component } from 'react'
import { Mutation } from 'react-apollo'
import gql from 'graphql-tag'

const POST_MUTATION = gql`
mutation postMutation($description: String!, $url: String!) {
  createNewsLink (input:{description:$description url:$url}) {
	newsLink{
      id
      createdAt
      description
      url
      userId
    }
  }
}

`



class CreateLink extends Component{

    state={
        description: '',
        url: ''
    };

    render(){
        const {description, url} = this.state

        return(
            <div>
                <div className = "flex flex-column mt3">
                    <input
                        className="mb2"
                        value={this.state.description}
                        onChange={e => this.setState({description : e.target.value})}
                        type="text"
                        placeholder="A description for the Link"/>
                    <input
                        className="mb2"
                        value={this.state.url}
                        onChange={e => this.setState({url: e.target.value})}
                        type="text"
                        placeholder="The URL for the link"/>
                </div>
                <Mutation mutation={POST_MUTATION}
                          variables={{ description, url }}
                            onCompleted={() => this.props.history.push('/')}>
                  {postMutation => <button onClick={postMutation}>Submit</button>}
                </Mutation>
            </div>
        )
    }
}

export default CreateLink
